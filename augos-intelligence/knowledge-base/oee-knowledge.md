# Augos Enhanced OEE — Complete Knowledge Reference

## The Founding Story: The Evolution of Truth

### The 2017 Challenge: A "Head-Scratcher"
For a decade, Augos (then QuantaPower) were the utility experts — measuring the electricity and water that kept global manufacturing alive. But in 2017, a food giant with 40 plants and 200 production lines handed them a challenge that didn't fit their toolkit: *"Measure our labor and capital productivity on an impossible budget."*

Coming from outside the insular world of manufacturing systems was Augos's greatest advantage. No "legacy bias." When they looked at OEE (Overall Equipment Effectiveness), the industry's holy grail, they didn't see a solution. They saw a **rearview mirror** — a vague, lagging indicator that told you that you lost, but never exactly how or why.

### The Evolutions

**Evolution 1 — Questioning the "Performance" Blur:**
The "Performance" metric in traditional OEE was a lie. It lumped machine speed and small stops together, creating a fog. Augos split "Small Stops" from "True Speed" and discovered that machines are actually quite predictable. The "silent killers" were the **Micro-Interruptions** — gaps in production so small they were invisible to the human eye, yet devastating in aggregate.

**Evolution 2 — From "Planning" to "Operator Discipline":**
Operators were often being held accountable for poor scheduling, not poor execution. Looking at a steel press in the motor industry, a routine coil change took 29 minutes on average but ranged from **6 minutes to nearly an hour and a half**. By splitting Planned Time into Allocated vs. Actual, Augos identified **Planning Efficiency**. They didn't just find losses; they found the **"Gold Standard" operators**. Today, data models identify the strongest operators for every SOP, so the best people can write the rules for everyone else.

**Evolution 3 — Solving the Accountability Crisis: The "Digital Signal":**
A recurring wall: the "blame game" between Production and Technical teams. When a machine stops, the clock just ticks away in ambiguity. Augos ended the debate by redefining Unplanned Stops through measuring the **Response**, not just the downtime:
- **Operator Resolution:** If the operator fixes it, they own the "Resolution %"
- **The Hand-off:** If they can't fix it, they send a **Digital Signal**
- **Technical Accountability:** The moment that signal is sent, the clock shifts — tracking Tech Response Time, Active Wrench Time vs. Inactive Wrench Time

By using **unique event QR codes that cannot be manipulated**, Augos replaced finger-pointing with a transparent "Loss Hierarchy."

### The Augos Manifesto: 11 Variables of Truth
Augos outgrew the name QuantaPower because they outgrew the mission. They don't just provide data; they provide a **complete diagnostic**. OEE has been decomposed into **11 actionable variables**. They don't ask, "What is your OEE?" They ask, **"Which lever are we pulling today?"** Guided by millisecond data to ask the only four questions that matter: **What, Who, Why, and When?**

---

## What is Enhanced OEE?

Traditional OEE gives you a single percentage. Enhanced OEE gives you a **complete diagnostic** — decomposing every hour of lost production into actionable, measurable variables.

The question is no longer *"what is our OEE?"* but **"which lever do we pull first?"**

---

## The OEE Loss Hierarchy

All production time that is not value-adding output is classified as loss. Enhanced OEE decomposes this loss through **6 levels** of increasing granularity.

### Level 0 — Total Loss
| Variable | Hours | % of Total |
|----------|-------|------------|
| Total Loss | 284h | 100% |

All OEE losses combined — 284 hours of production never recovered.

---

### Level 1 — OEE Categories (A · P · Q)
The standard three categories of OEE loss. This is where traditional OEE stops — Augos goes five levels deeper.

| Category | Hours | % of Total | Color |
|----------|-------|------------|-------|
| **Availability** | 186h | 65% | Amber (#F59E0B) |
| **Performance** | 72h | 25% | Blue (#3B82F6) |
| **Quality** | 26h | 9% | Purple (#8B5CF6) |

**Narrative:** Traditional OEE gives you three categories. Useful — but not enough to act on. Where inside these 284 hours can you actually intervene?

---

### Level 2 — Sub-Categories
Availability splits into Planned vs Unplanned downtime. Performance and Quality pass through.

| Sub-Category | Parent | Hours | % of Total | Color |
|-------------|--------|-------|------------|-------|
| **Planned** | Availability | 42h | 15% | Dark Amber (#D97706) |
| **Unplanned** | Availability | 144h | 51% | Rose (#F43F5E) |
| **Performance** | Performance | 72h | 25% | Blue (#3B82F6) |
| **Quality** | Quality | 26h | 9% | Purple (#8B5CF6) |

**Narrative:** Not all Availability loss is the same. 42 hours were planned downtime that overran. 144 hours were completely unplanned. That distinction changes everything.

---

### Level 3 — Resolution Path
Who resolved the issue — operator or technician? This is where the **Digital Signal** concept comes in — ending the blame game between Production and Technical teams.

| Variable | Parent | Hours | % of Total | Color |
|----------|--------|-------|------------|-------|
| **Planning Efficiency** | Planned | 28h | 10% | Gold (#CA8A04) |
| **Operator Discipline** | Planned | 14h | 5% | Yellow (#FBBF24) |
| **Operator Resolved** | Unplanned | 58h | 20% | Orange (#FB923C) |
| **Tech Intervention** | Unplanned | 86h | 30% | Red (#DC2626) |
| **Performance** | Performance | 72h | 25% | Blue (#3B82F6) |
| **Quality** | Quality | 26h | 9% | Purple (#8B5CF6) |

**Narrative:** The operator fixed it themselves — or they had to call a technician. 58 hours resolved on the floor. 86 hours required technical intervention. Now you know where to train and where to invest.

**Origin Story:** This split was born from the "accountability crisis" — the recurring blame game between Production and Technical teams. Augos replaced ambiguity with a transparent handoff mechanism using unique event QR codes.

---

### Level 4 — Time Account
Every minute classified. Technical Intervention, Performance, and Quality each decompose.

| Variable | Parent | Hours | % of Total | Color |
|----------|--------|-------|------------|-------|
| **Planning Efficiency** | Planned | 28h | 10% | Gold (#CA8A04) |
| **Operator Discipline** | Planned | 14h | 5% | Yellow (#FBBF24) |
| **Operator Resolution** | Unplanned | 58h | 20% | Orange (#FB923C) |
| **Operator Evaluation** | Tech Intervention | 10h | 4% | Pink (#FB7185) |
| **Tech Response** | Tech Intervention | 16h | 6% | Red (#EF4444) |
| **Wrench Time** | Tech Intervention | 60h | 21% | Teal (#14B8A6) |
| **Micro Interruptions** | Performance | 24h | 8% | Light Blue (#60A5FA) |
| **True Speed Loss** | Performance | 48h | 17% | Indigo (#6366F1) |
| **Startup Rejects** | Quality | 14h | 5% | Violet (#A855F7) |
| **In-Process Rejects** | Quality | 12h | 4% | Pink (#EC4899) |

**Narrative:** Technical intervention breaks down into evaluation, waiting, and actual repair. Performance reveals micro-stoppages and speed loss. Quality splits into startup and in-process rejects. Every minute classified.

---

### Level 5 — The Science (Final Decomposition)
11 variables. Each measurable. Each actionable.

| # | Variable | Parent | Hours | % of Total | Color | Description | Origin |
|---|----------|--------|-------|------------|-------|-------------|--------|
| 1 | **Planning Efficiency** | Planned | 28h | 10% | #CA8A04 | Hours lost to scheduling inefficiency — planned downtime that overran its allocation | Born from a steel press study: coil changes ranged from 6 min to 90 min. Allocated vs. Actual reveals the scheduling gap. |
| 2 | **Operator Discipline** | Planned | 14h | 5% | #FBBF24 | Late starts, early stops, extended breaks | Operators were being blamed for scheduling problems. This variable isolates genuine operator time discipline from planning failures. |
| 3 | **Operator Resolution Time** | Unplanned | 58h | 20% | #FB923C | Operators resolving issues without technical support | If the operator fixes the machine, they own the "Resolution %" — this encourages frontline capability. |
| 4 | **Operator Evaluation Time** | Tech Intervention | 10h | 4% | #FB7185 | Diagnosing failures before calling for help | The clock between the stop event and the Digital Signal — how long does the operator evaluate before escalating? |
| 5 | **Tech Response Time** | Tech Intervention | 16h | 6% | #EF4444 | Waiting for technicians to arrive | From Digital Signal to technician arrival — pure accountability via QR-coded handoff. |
| 6 | **Active Wrench Time** | Wrench Time | 38h | 13% | #10B981 | Productive repair — the only "good" unplanned time — tools on machine | The portion where a technician is actually fixing the problem. |
| 7 | **Inactive Wrench Time** | Wrench Time | 22h | 8% | #EAB308 | Wrench time wasted on waiting for parts, searching, walking | The hidden waste within maintenance — technician present but not productive. |
| 8 | **Micro Interruptions** | Performance | 24h | 8% | #60A5FA | Micro-stops too brief to log but devastating in aggregate — the "silent killers" | Augos's first breakthrough discovery: machines are predictable; these invisible gaps are the true performance destroyers. |
| 9 | **True Speed Loss** | Performance | 48h | 17% | #6366F1 | Running below design speed — the silent killer | Separated from Small Stops in Evolution 1 — traditional OEE's "Performance" was a blur that hid this. |
| 10 | **Startup Rejects** | Quality | 14h | 5% | #A855F7 | Reject production during startup and changeover | Material wasted before the process stabilizes. |
| 11 | **In-Process Rejects** | Quality | 12h | 4% | #EC4899 | Steady-state defects during normal production | Defects that occur even when the process is "running correctly." |

**Narrative:** 11 variables. Each measurable. Each actionable. This is what Enhanced OEE reveals — not a single number, but a complete diagnostic. The question is no longer "what is our OEE?" but "which lever do we pull first?"

---

## Complete Hierarchy Tree

```
Total Loss (284h)
├── Availability (186h · 65%)
│   ├── Planned (42h · 15%)
│   │   ├── Planning Efficiency (28h · 10%)  ← Allocated vs Actual
│   │   └── Operator Discipline (14h · 5%)   ← Late starts, early stops
│   └── Unplanned (144h · 51%)
│       ├── Operator Resolved (58h · 20%)     ← Fixed without tech help
│       └── Tech Intervention (86h · 30%)     ← Digital Signal triggered
│           ├── Operator Evaluation (10h · 4%)  ← Before the signal
│           ├── Tech Response (16h · 6%)        ← After the signal
│           └── Wrench Time (60h · 21%)         ← Technician on-site
│               ├── Active Wrench (38h · 13%)   ← Tools on machine
│               └── Inactive Wrench (22h · 8%)  ← Waiting, searching
├── Performance (72h · 25%)
│   ├── Micro Interruptions (24h · 8%)  ← The silent killers
│   └── True Speed Loss (48h · 17%)     ← Below design speed
└── Quality (26h · 9%)
    ├── Startup Rejects (14h · 5%)
    └── In-Process Rejects (12h · 4%)
```

---

## The Four Questions

Augos is guided by millisecond data to ask the only four questions that matter:

| Question | What It Reveals | Example |
|----------|----------------|---------|
| **What** | Which of the 11 variables is consuming the most time? | True Speed Loss: 48h (17%) |
| **Who** | Is it an operator issue, a technician issue, or a planning issue? | Operator Evaluation: 10h before escalating — training opportunity |
| **Why** | Root cause within the variable | Coil changes averaging 29 min but ranging 6–90 min |
| **When** | Time patterns — shift, day, season | Night shifts show 2.3× the Inactive Wrench Time |

---

## The Gold Standard Operator Concept

One of the most powerful outcomes of Enhanced OEE: by decomposing every SOP into timed steps, Augos identifies the **strongest operators** for every procedure. Rather than training to an average, the best performers' methods become the benchmark — so your best people can write the rules for everyone else.

This transforms OEE from a blame instrument into a **coaching framework**.

---

## Key Insights

### Availability Dominates
Availability accounts for **65% of all loss** (186h). Within that, **Unplanned downtime** is 3.4× larger than Planned (144h vs 42h). This is the primary battleground.

### The Unplanned Breakdown
Of the 144 hours of unplanned downtime:
- **58h** were resolved by operators themselves (no technician needed)
- **86h** required technical intervention
  - Of which only **38h** was productive repair (Active Wrench)
  - **48h** was overhead: evaluation (10h), waiting for response (16h), and inactive wrench time (22h)

### The Silent Killers
Performance loss is subtle — the machine runs, but slowly. **True Speed Loss** alone (48h) is larger than all of Planned downtime (42h). Micro Interruptions (24h) are individually invisible but collectively devastating. This was Augos's first breakthrough: traditional OEE's "Performance" metric was a blur that hid these two fundamentally different problems.

### Quality is the Smallest — But Not Negligible
At 26h (9%), Quality loss is the smallest category. But each hour represents wasted material, energy, and labour on product that can never be sold.

### The Accountability Shift
The Digital Signal mechanism — unique, non-manipulable QR codes — replaces finger-pointing with transparent timestamps. Every transition of responsibility is recorded to the millisecond.

---

## The Operator Interface (HMI)

The operator interacts with a **10" or 15" HMI touch terminal** mounted at the production line. The interface has distinct modes:

### While Running
The operator sees **real-time statistical data on productivity** — the machine is producing, the system is counting.

### When Production Stops
The screen shifts to a **stoppage state**. The flow:

1. **Small Stop Countdown** — A timer counts down based on the customer-defined Small Stop threshold (e.g., anything under 2 minutes doesn't need a reason and is automatically classified as a "Micro Interruption").

2. **Beyond Threshold — Mandatory Stop Selection** — If the stop exceeds the threshold, the operator **must** select a stoppage reason. The interface provides a **structured drill-down of >500 stoppage reasons in just 3 touches** — no scrolling, no manual text input.

3. **Planned Stop** — Screen shows a **countdown** using the stoppage type's allocated time, showing time remaining to complete. This is how Planning Efficiency is measured — allocated vs actual.

4. **Unplanned Stop** — Screen **counts up**, showing time in stop. The operator can attempt to resolve.

5. **The "Assist" Button** — At any point the operator can hit **"Assist"**. This:
   - Triggers a message on the technician's **Assist app**
   - Generates a **unique QR code** on the operator terminal
   - This is the **Digital Signal** — the formal hand-off

6. **Proof of Presence** — The technician must scan the QR code to validate they are physically at the fault. This precisely timestamps:
   - **Tech Response Time** (Digital Signal → QR scan)
   - **Wrench Time** begins at QR scan (tools-on)

### Why This Matters
The interface captures the full response chain without relying on manual logs. By embedding stoppage classification into the machine stop itself (not after the fact), every second is accounted for with precision.

---

## Key Mechanisms

### The Digital Signal
When an operator cannot resolve a machine stop, they hit "Assist" which generates a **unique event QR code** on the HMI. This creates an unmanipulable timestamp that:
1. Records when the operator gave up self-resolution (Operator Evaluation Time ends)
2. Sends an alert to the technician's Assist app
3. Starts the clock on Tech Response Time
4. Cannot be back-dated or manipulated
5. The technician's QR scan creates **proof-of-presence** — confirming physical arrival

### Single Measurement Point Architecture
Each production line uses a **single measurement point** for production output. This is fundamentally different from traditional MES systems that rely on multiple diagnostic sensors. Augos pairs this single signal with a structured touch interface to capture the **context** that sensors cannot:
- Why the machine stopped (operator-classified from >500 reasons)
- Who resolved it and how
- Environmental factors (waiting for forklift, out of packing material, etc.)

### What MES Systems Miss
Traditional MES solutions are limited to the number of sensor endpoints and digital values. This means:
- Granularity is lost — only the measurable parts of the process are measured
- They can't sense that you're **waiting for a forklift** or have **run out of packing material**
- The real-world environmental impacts on production are invisible

Augos brings these real-world impacts into the equation alongside the machine data.

### Data Collection
The Augos platform calculates the 11 variables automatically from:
- Single production measurement point per line
- Operator interaction logs via HMI (>500 classified stoppage reasons)
- QR-coded proof-of-presence events
- Shift schedules and calendar data
- Speed setpoints vs actuals
- Millisecond-resolution timestamps

---

## Field Deployment: The 2017 FMCG Rollout

### Scale
Deployed across **50 production lines** at a major food manufacturer with 40 plants. The system delivered three things exceptionally well:
1. **Full digitisation** of downtime events
2. **Full account of every second** of paid time — every stop precise in duration
3. **Simplified over-the-air management** of system variables — low cost, fast deployment at scale

### Adoption Reality
Outcomes varied tremendously from site to site, **largely dependent on management commitment**. As a top-down decision, some sites adopted fully while others did not. This is a critical insight: the technology works — the variable is leadership.

### Field Case Studies

#### (a) The Ginger Ale Discovery
**Plant:** Carbonated fizzy drink plant, 2L filling machine
**Problem:** Losses varied dramatically on a single SKU — Ginger Ale — while all other products (Cola, etc.) ran essentially the same. This defied logic.
**Data Insight:** The data forced a deeper dive. Analysis revealed a **higher sugar content** in the Ginger Ale was causing the liquid to fizz during filling, creating overflows and underfills that didn't occur with other SKUs.
**Resolution:** A small adjustment in fill rate on this product resolved the issue.
**Lesson:** Without granular data, this would have remained an unexplained anomaly. The system exposed a formulation-dependent production variable.

#### (b) The Packaging Cost Inversion
**Plant:** Condiments producer — white label tomato sauce and chutney for multiple retailers
**Setup:** Same formula, differentiated packaging — premium glass bottles vs lower-cost plastic packaging on the same production line.
**Discovery:** The premium glass bottles ran **near faultlessly**, while the cheaper plastic packaging was impacted by **systemic small stops** (Micro Interruptions). The accumulation of these micro-stops meant that **the cost of supplying the cheaper plastic solution was higher than the premium glass bottle** due to productivity losses.
**Lesson:** Without the Micro Interruptions variable, this cost inversion would have been invisible. The "cheaper" packaging was actually the expensive one when total cost of production was considered.

#### (c) The Human Element
**Observation:** Same line, different operator. Same task, different operator. Same unplanned stop, different operator. The data made it undeniable that **the human element is a fundamental differentiator**.
**Analogy:** Like sport — there are 1st team players and everyone else. The consistency of your operation is critically dependent on people.
**Impact:** This led directly to the Gold Standard Operator concept — identifying the best performers for each SOP and using their methods as the benchmark.

#### (d) The R350k vs R70k Problem — The Batch Date Coder
**Plant:** FMCG production line
**Problem:** Recurring stops in the 2–10 minute range on a batch date coder. To the operator, this was not a major fault — it was within their capability to solve, and the stops never held the line up long enough for anyone to pay attention.
**Data Insight:** But the **accumulation of time was significant**. A quick calculation of lost margin showed that the impact on profit over a single week was **5× greater than a new and upgraded batch date coder** — **R350,000 in losses for a R70,000 solve**.
**Lesson:** Budgets get in the way of obvious fixes. The data provides clarity for action, not anecdote. The unseen cost of stops vs the cost of resolution — this is the power of quantification.

#### (e) The Operator's Voice
**Observation:** Operators know significantly more about productivity impacts than management, but **they do not have the voice to share the most critical information**.
**Pattern:** In every post-installation presentation, when diving into the numbers, leadership had a keen understanding of output but **no real idea of the friction and systemic issues**. A digital translation of losses makes this clear and gives the operator a voice in the boardroom.
**Impact:** Leaders don't know, and operators can't always communicate the impact. This data layer becomes the **nexus for specific issue prioritisation and engagement**.

#### (f) Do Management Get In The Way?
**Finding:** Almost all operations that ran like-sized shifts had **higher output in the evening shifts**.
**Implication:** Management presence during day shifts may actually introduce friction. Evening shifts, with more operator autonomy, consistently outperformed.

#### (g) The 95% Rule
**Critical Finding:** With exceptional cases aside, **Speed and Quality combined account for less than 5% of losses. Availability is everything.**
**Implication:** This radically simplifies the problem. The vast majority of recoverable production time is lost to stoppages — not to slow running or defects. Focus on Availability first, always.

---

## Deployment & Pricing Model

### How Augos Deploys
- **No big capex or project commitments** — as close to plug-and-play as possible
- Implementation and management is **clean, fast, and simple**
- Single measurement point per production line
- Over-the-air management of system variables
- Rapid realisation of value — low cost of deployment

### Pricing Position
- Not a "cheap" option — pricing reflects quality of product and level of service
- **Better priced** than alternative MES solutions
- **Greater value and insight** than traditional approaches
- **Easier to deploy** — no complex integration projects
- All of which leads to rapid ROI

### Competitive Advantage vs Traditional MES
| Dimension | Traditional MES | Augos |
|-----------|----------------|-------|
| **Measurement** | Multiple sensors per line | Single production point + structured HMI |
| **Stoppage Context** | Limited to sensor values | >500 reasons in 3 touches |
| **Environmental Factors** | Cannot detect (forklift delays, material shortages) | Operator-classified in real-time |
| **Deployment** | Heavy integration project | Plug-and-play, over-the-air config |
| **Cost** | High capex + project fees | Lower cost, rapid ROI |
| **Granularity** | Limited by sensor count | 11 variables from single point + operator context |
| **Human Factors** | Not captured | Operator variability, discipline, evaluation time |

---

## Company Context

| Detail | Value |
|--------|-------|
| **Current Name** | Augos |
| **Previous Name** | QuantaPower |
| **Name Change Reason** | Outgrew the utility-only mission — now a complete manufacturing diagnostic platform |
| **Origin** | Utility measurement (electricity & water) for global manufacturing |
| **Pivotal Moment** | 2017 — food giant with 40 plants, 200 lines, impossible budget |
| **Initial Deployment** | 50 production lines across multiple sites |
| **Key Advantage** | No legacy bias — came from outside insular manufacturing systems |
| **Core Innovation** | Decomposing OEE into 11 actionable variables |
| **Guiding Questions** | What, Who, Why, When |
| **Data Resolution** | Millisecond |
| **Anti-Manipulation** | Unique event QR codes with proof-of-presence |
| **HMI Interface** | 10" or 15" touch terminal per production line |
| **Stoppage Classification** | >500 reasons in 3 touches, no scrolling |
| **Quality Position** | Quality is difficult (waste, reworks, varying perspectives) and typically <5% of losses — not a primary focus |

---

## Brand Assets

### Logo
- **File:** `augos-logo.png` (2880 × 649px, RGBA PNG)
- **Design:** Black triangle with blue accent (the "A" icon) + "AUGOS™" wordmark
- **Icon Colors:** Black triangle, blue (#3B82F6 approx) accent at base
- **Wordmark:** Clean, modern sans-serif, all caps

### Additional Assets (Google Drive — require authentication)
- Logo reference: `1pV3DB7uURH5PUald432wyL2IfhkpoR0s` ("best reference")
- Asset 1: `1ltDO1zQNtbxvkOv8VKjSUENjhneyiWzX`
- Asset 2: `1-RqhtBhn-L7q5yBwT4jgh-E3UTSVijtE`
- Brand folder: `11HPDzJy9vCaX634_AQRqFfRj2Q31I-aB`

---

## Visualization Index

The following HTML visualizations exist in `knowledge-base-web/`:

| File | Type | Description |
|------|------|-------------|
| `oee-hierarchy-morph.html` | **Scroll-Driven Morph** | Single bar splits through 5 levels on scroll. Narrative H2 + copy at each level. |
| `oee-hierarchy-scroll.html` | **Scroll-Driven Morph (Alt)** | Alternative scroll morph with step dots and collision-avoidant labels. |
| `oee-waterfall-animated.html` | **Scroll-Driven Waterfall** | Bars reveal one-by-one as you scroll. Opens with "284 hours" intro. Story callouts per bar. |
| `oee-waterfall-bar-v1.html` | **Static Waterfall V1** | Full-width waterfall with feint connector lines. |
| `oee-waterfall-bar-v2.html` | **Static Waterfall V2** | Full-width waterfall with gradient shading zones. |
| `oee-waterfall-bar-v3.html` | **Static Waterfall V3** | Three-layer: A·P·Q → Sub-categories → 11 variables. |
| `oee-sankey.html` | **Sankey Diagram** | Flow-based visualization of loss decomposition. |
| `oee-matrix.html` | **Matrix Heatmap** | OEE matrix view. |
| `oee-dimensions.html` | **Surface vs Intelligence** | Comparing standard vs enhanced OEE dimensions. |
| `oee-sunburst.html` | **Sunburst Chart** | Radial hierarchical breakdown. |
| `oee-treemap.html` | **Treemap** | Area-based hierarchical view. |
| `oee-icicle.html` | **Icicle Chart** | Inverted tree visualization. |
| `oee-circle-packing.html` | **Circle Packing** | Nested circle hierarchy. |
| `oee-radial-bar.html` | **Radial Bar** | Polar bar chart variant. |
| `oee-stream.html` | **Streamgraph** | Time-series flow visualization. |
| `oee-cascade-bars.html` | **Cascade Bars** | Cascading bar decomposition. |
| `oee-drill-doughnut.html` | **Drilldown Doughnut** | Interactive doughnut with drill-through. |
| `oee-hierarchy-connected.html` | **Connected Hierarchy** | Multi-level bar chart with bezier connectors. |
| `oee-matrix-evolution.html` | **Matrix Evolution** | Time-evolving heatmap. |

---

## Design System

### Color Palette (OEE Categories)

| Category | Primary | Hex |
|----------|---------|-----|
| Availability | Amber | `#F59E0B` |
| Planned | Dark Amber | `#D97706` |
| Unplanned | Rose | `#F43F5E` |
| Performance | Blue | `#3B82F6` |
| Quality | Purple | `#8B5CF6` |
| Active Wrench (positive) | Emerald | `#10B981` |
| Inactive Wrench (waste) | Yellow | `#EAB308` |

### Typography
- **Headings:** Space Grotesk (600/700 weight)
- **Body:** Inter (300–600 weight)
- **Data/Labels:** JetBrains Mono (400/500 weight)

### Background
- Primary: `#06080A` (near-black)
- Canvas/Surface: `rgba(255,255,255,0.012)`
- Accent: `#F59E0B` (amber glow)

---

## Data Source Note

The example data in all visualizations uses a **284-hour total loss** scenario across a production period. This data is representative and can be substituted with actual plant data from the Augos platform.
