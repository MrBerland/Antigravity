/**
 * Augos Report Audit — Automated Screenshot & Data Extraction
 * 
 * Usage:
 *   1. npm install playwright (one-time)
 *   2. node audit-reports.js
 * 
 * What it does:
 *   - Opens a browser with your existing Augos session cookies
 *   - Visits each report URL for the target point
 *   - Scrolls through the full page in viewport-height increments
 *   - Captures numbered screenshots at each scroll position
 *   - Extracts all headings, tables, buttons, charts, exports from the DOM
 *   - Saves everything to the report-audit folder structure
 * 
 * Cost: $0 — runs locally on your Mac
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// ─── Configuration ───────────────────────────────────────────────────────────

const BASE_URL = 'https://dev.live.augos.io/app/utilities-and-services';
const POINT_ID = '8323';
const PRODUCT_ID = '1';
const OUTPUT_DIR = path.join(__dirname, '..');

// Reports to audit — set `skip: true` for already-completed ones
const REPORTS = [
  { slug: 'dashboard', name: 'Dashboard', folder: '01-dashboard', skip: true },
  { slug: 'technical-analysis', name: 'Technical Analysis', folder: '02-technical-analysis', skip: true },
  { slug: 'consumption-breakdown', name: 'Consumption Breakdown', folder: '03-consumption-breakdown', skip: true },
  { slug: 'cost-breakdown', name: 'Cost Breakdown', folder: '04-cost-breakdown', skip: false }, // Re-run for comparison
  { slug: 'cost-allocation', name: 'Cost Allocation', folder: '05-cost-allocation', skip: true },
  { slug: 'bill-verification', name: 'Bill Verification', folder: '06-bill-verification', skip: true },
  { slug: 'power-factor-and-demand', name: 'Power Factor & Demand', folder: '07-power-factor-demand', skip: true },
  { slug: 'time-of-use', name: 'Time of Use', folder: '08-time-of-use', skip: true },
  { slug: 'tariff-comparison', name: 'Tariff Comparison', folder: '09-tariff-comparison', skip: true },
  { slug: 'load-curtailment', name: 'Load Curtailment', folder: '10-load-curtailment', skip: true },
  { slug: 'charting', name: 'Charting', folder: '11-charting', skip: false },
  { slug: 'data-download', name: 'Data Download', folder: '12-data-download', skip: false },
  { slug: 'triggers', name: 'Triggers', folder: '13-triggers', skip: false },
];

// ─── DOM Extraction Script ───────────────────────────────────────────────────

const EXTRACT_SCRIPT = `
(() => {
  const getRect = (el) => {
    const r = el.getBoundingClientRect();
    return { top: r.top, left: r.left, width: r.width, height: r.height };
  };

  return JSON.stringify({
    title: document.title,
    url: window.location.href,
    timestamp: new Date().toISOString(),
    pageHeight: document.body.scrollHeight,
    viewportHeight: window.innerHeight,
    viewportWidth: window.innerWidth,

    // All headings
    headings: Array.from(document.querySelectorAll('h1,h2,h3,h4,h5')).map(e => ({
      tag: e.tagName,
      text: e.textContent.trim().substring(0, 200),
      rect: getRect(e)
    })),

    // All tables with full structure
    tables: Array.from(document.querySelectorAll('table')).map((t, i) => ({
      index: i,
      headers: Array.from(t.querySelectorAll('th')).map(th => th.textContent.trim().substring(0, 100)),
      rowCount: t.querySelectorAll('tbody tr').length,
      sampleRows: Array.from(t.querySelectorAll('tbody tr')).slice(0, 5).map(tr =>
        Array.from(tr.querySelectorAll('td')).map(td => td.textContent.trim().substring(0, 80))
      ),
      allRows: Array.from(t.querySelectorAll('tbody tr')).map(tr =>
        Array.from(tr.querySelectorAll('td')).map(td => td.textContent.trim().substring(0, 80))
      ),
      rect: getRect(t)
    })),

    // Charts (canvas + SVG)
    charts: Array.from(document.querySelectorAll('canvas, svg[class], [class*="chart"], [class*="graph"], [class*="recharts"]')).map(e => ({
      tag: e.tagName,
      className: (e.className || '').toString().substring(0, 100),
      width: e.offsetWidth,
      height: e.offsetHeight,
      rect: getRect(e)
    })).filter(c => c.width > 50 && c.height > 50).slice(0, 30),

    // Buttons
    buttons: Array.from(document.querySelectorAll('button')).map(e => ({
      text: e.textContent.trim().substring(0, 100),
      disabled: e.disabled,
      ariaLabel: e.getAttribute('aria-label')
    })).filter(b => b.text.length > 0 && b.text.length < 100),

    // Tabs
    tabs: Array.from(document.querySelectorAll('[role="tab"], [class*="tab"]')).map(e => ({
      text: e.textContent.trim().substring(0, 80),
      active: e.classList.contains('active') || e.getAttribute('aria-selected') === 'true',
      className: (e.className || '').substring(0, 100)
    })).filter(t => t.text.length > 0 && t.text.length < 80),

    // Export/download buttons  
    exports: Array.from(document.querySelectorAll('button, a')).filter(e => {
      const t = (e.textContent || '').toLowerCase();
      return t.includes('download') || t.includes('export') || t.includes('xlsx') || 
             t.includes('csv') || t.includes('ai') || t.includes('copy');
    }).map(e => ({
      tag: e.tagName,
      text: e.textContent.trim().substring(0, 100),
      href: e.href || null
    })),

    // Section banners (Augos uses colored header bars)
    sectionBanners: Array.from(document.querySelectorAll('[class*="banner"], [class*="header"], [class*="section"]')).filter(e => {
      const text = e.textContent.trim();
      return text.length > 2 && text.length < 100 && e.offsetHeight > 20 && e.offsetHeight < 80;
    }).map(e => ({
      text: e.textContent.trim().substring(0, 100),
      bgColor: window.getComputedStyle(e).backgroundColor,
      rect: getRect(e)
    })).slice(0, 20),

    // KPI cards (common in Augos reports)
    kpiCards: Array.from(document.querySelectorAll('[class*="card"], [class*="kpi"], [class*="metric"], [class*="stat"]')).filter(e => {
      return e.offsetWidth > 100 && e.offsetHeight > 50 && e.offsetHeight < 300;
    }).map(e => ({
      text: e.textContent.trim().substring(0, 200),
      className: (e.className || '').substring(0, 100),
      rect: getRect(e)
    })).slice(0, 20),

    // Select/dropdown elements
    selects: Array.from(document.querySelectorAll('select, [class*="select"], [class*="dropdown"]')).map(e => ({
      text: e.textContent.trim().substring(0, 200),
      options: Array.from(e.querySelectorAll('option')).map(o => o.textContent.trim()).slice(0, 20),
      className: (e.className || '').substring(0, 100)
    })).slice(0, 10),

    // Date pickers
    datePickers: Array.from(document.querySelectorAll('input[type="date"], input[type="datetime-local"], [class*="date"], [class*="picker"]')).map(e => ({
      type: e.type,
      value: e.value,
      placeholder: e.placeholder,
      className: (e.className || '').substring(0, 100)
    })).slice(0, 10),

    // Visible text content snapshot (first 5000 chars of body text)
    bodyTextSnapshot: document.body.innerText.substring(0, 5000),

    // Empty state detection
    hasEmptyState: /no data|not configured|empty|no results|not set up/i.test(document.body.innerText)
  }, null, 2);
})()
`;

// ─── Main ────────────────────────────────────────────────────────────────────

async function main() {
  console.log('🔧 Launching browser...');

  // Launch with user data dir to reuse existing login session
  const browser = await chromium.launchPersistentContext(
    path.join(process.env.HOME, 'Library/Application Support/Google/Chrome/Default'),
    {
      headless: false,
      viewport: { width: 1512, height: 780 },
      channel: 'chrome', // Use installed Chrome (has cookies)
      args: ['--no-first-run', '--no-default-browser-check'],
    }
  );

  const page = await browser.newPage();

  const pendingReports = REPORTS.filter(r => !r.skip);
  console.log(`\n📋 Auditing ${pendingReports.length} reports:\n`);
  pendingReports.forEach(r => console.log(`   → ${r.name}`));
  console.log('');

  for (const report of pendingReports) {
    const url = `${BASE_URL}/${report.slug}?pointId=${POINT_ID}&productId=${PRODUCT_ID}`;
    const reportDir = path.join(OUTPUT_DIR, report.folder);
    const screenshotDir = path.join(reportDir, 'playwright');

    // Ensure directories exist
    fs.mkdirSync(screenshotDir, { recursive: true });

    console.log(`\n${'═'.repeat(60)}`);
    console.log(`📊 ${report.name}`);
    console.log(`   URL: ${url}`);
    console.log(`${'═'.repeat(60)}`);

    // Navigate and wait for load
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    } catch (e) {
      console.log(`   ⚠️  Network idle timeout — continuing (page likely loaded)`);
    }

    // Extra wait for charts/animations
    await page.waitForTimeout(3000);

    // ── Extract DOM data ──
    console.log('   📝 Extracting DOM structure...');
    let extractedData;
    try {
      const rawData = await page.evaluate(EXTRACT_SCRIPT);
      extractedData = JSON.parse(rawData);
    } catch (e) {
      console.log(`   ⚠️  Extraction error: ${e.message}`);
      extractedData = { error: e.message };
    }

    // Save extracted data
    const dataFile = path.join(reportDir, `${report.slug}-data.json`);
    fs.writeFileSync(dataFile, JSON.stringify(extractedData, null, 2));
    console.log(`   💾 Data saved: ${report.slug}-data.json`);

    // ── Scroll & Screenshot ──
    const pageHeight = extractedData.pageHeight || 3000;
    const viewportHeight = extractedData.viewportHeight || 780;
    const scrollSteps = Math.ceil(pageHeight / (viewportHeight * 0.85)); // 85% overlap

    console.log(`   📸 Capturing ${scrollSteps} screenshots (page: ${pageHeight}px)...`);

    for (let i = 0; i < scrollSteps; i++) {
      const scrollY = i * Math.floor(viewportHeight * 0.85);
      await page.evaluate(`window.scrollTo(0, ${scrollY})`);
      await page.waitForTimeout(500); // Let animations settle

      const screenshotName = `${String(i + 1).padStart(2, '0')}-scroll-${scrollY}px.png`;
      const screenshotPath = path.join(screenshotDir, screenshotName);
      await page.screenshot({ path: screenshotPath, fullPage: false });
      console.log(`   ✅ ${screenshotName}`);
    }

    // Also capture a full-page screenshot
    const fullPagePath = path.join(screenshotDir, '00-full-page.png');
    await page.screenshot({ path: fullPagePath, fullPage: true });
    console.log(`   ✅ 00-full-page.png (full page)`);

    // ── Interactive elements: click tabs and capture each view ──
    console.log('   🔄 Discovering interactive tabs...');

    const tabElements = await page.$$('[role="tab"], [class*="MuiTab"], [class*="tab-item"], [class*="nav-link"]');
    const tabTexts = [];
    for (const tab of tabElements) {
      const text = await tab.textContent().catch(() => '');
      if (text.trim().length > 0 && text.trim().length < 80) tabTexts.push(text.trim());
    }

    if (tabTexts.length > 1) {
      console.log(`   📑 Found ${tabTexts.length} tabs: ${tabTexts.join(', ')}`);

      const interactiveDir = path.join(screenshotDir, 'tabs');
      fs.mkdirSync(interactiveDir, { recursive: true });

      const tabData = [];

      for (let t = 0; t < tabElements.length; t++) {
        const tabText = tabTexts[t] || `tab-${t}`;
        const safeName = tabText.replace(/[^a-zA-Z0-9]/g, '-').toLowerCase().substring(0, 40);

        try {
          // Click the tab
          await tabElements[t].click();
          await page.waitForTimeout(1500); // Wait for content to render

          // Scroll to top of section and screenshot
          await page.evaluate('window.scrollTo(0, 0)');
          await page.waitForTimeout(300);

          // Capture full page for this tab view
          const tabScreenshot = path.join(interactiveDir, `${String(t + 1).padStart(2, '0')}-${safeName}.png`);
          await page.screenshot({ path: tabScreenshot, fullPage: true });
          console.log(`   ✅ Tab "${tabText}" captured`);

          // Extract data in this tab state
          const tabExtract = await page.evaluate(EXTRACT_SCRIPT).catch(() => '{}');
          tabData.push({
            tabName: tabText,
            tabIndex: t,
            data: JSON.parse(tabExtract)
          });
        } catch (e) {
          console.log(`   ⚠️  Tab "${tabText}" click failed: ${e.message}`);
        }
      }

      // Save tab interaction data
      const tabDataFile = path.join(reportDir, `${report.slug}-tabs.json`);
      fs.writeFileSync(tabDataFile, JSON.stringify(tabData, null, 2));
      console.log(`   💾 Tab data saved: ${report.slug}-tabs.json`);
    } else {
      console.log('   ℹ️  No interactive tabs found');
    }

    // ── Try expanding accordion/collapsible rows ──
    console.log('   🔽 Checking for expandable rows...');
    const expandableRows = await page.$$('tr[class*="expand"], tr[class*="clickable"], tr[style*="cursor: pointer"], [class*="accordion"], [class*="collapsible"]');

    if (expandableRows.length > 0) {
      console.log(`   📂 Found ${expandableRows.length} expandable elements`);
      const expandDir = path.join(screenshotDir, 'expanded');
      fs.mkdirSync(expandDir, { recursive: true });

      // Click first 3 expandable items
      for (let e = 0; e < Math.min(expandableRows.length, 3); e++) {
        try {
          await expandableRows[e].scrollIntoViewIfNeeded();
          await expandableRows[e].click();
          await page.waitForTimeout(1000);

          await page.screenshot({
            path: path.join(expandDir, `expanded-${e + 1}.png`),
            fullPage: false
          });
          console.log(`   ✅ Expanded row ${e + 1} captured`);

          // Click again to collapse
          await expandableRows[e].click();
          await page.waitForTimeout(500);
        } catch (err) {
          console.log(`   ⚠️  Expand row ${e + 1} failed: ${err.message}`);
        }
      }
    } else {
      console.log('   ℹ️  No expandable rows found');
    }

    console.log(`   ✨ ${report.name} — done!`);
  }

  console.log(`\n${'═'.repeat(60)}`);
  console.log(`🎉 All ${pendingReports.length} reports audited!`);
  console.log(`📁 Output: ${OUTPUT_DIR}`);
  console.log(`${'═'.repeat(60)}\n`);

  await browser.close();
}

main().catch(console.error);
