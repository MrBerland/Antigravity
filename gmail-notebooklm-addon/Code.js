/**
 * Entry point for the Gmail Add-on.
 * Triggered when an email is opened.
 */
function getContextualAddOn(e) {
    // Guard against manual execution in Editor
    if (!e || !e.messageMetadata) {
        console.error("Error: getContextualAddOn was run manually. usage: Open an email in Gmail to trigger this.");
        return CardService.newCardBuilder()
            .setHeader(CardService.newCardHeader().setTitle("Error"))
            .addSection(CardService.newCardSection().addWidget(CardService.newTextParagraph().setText("Please open an email to use this add-on.")))
            .build();
    }

    const messageId = e.messageMetadata.messageId;
    const accessToken = e.messageMetadata.accessToken;
    GmailApp.setCurrentMessageAccessToken(accessToken);

    return createMainCard(messageId);
}

/**
 * Creates the main card interface.
 */
function createMainCard(messageId) {
    const card = CardService.newCardBuilder();

    // Header
    const header = CardService.newCardHeader()
        .setTitle('NotebookLM Connector')
        .setSubtitle('Save context for NotebookLM')
        .setImageUrl('https://www.gstatic.com/images/icons/material/system/1x/save_black_24dp.png')
        .setImageStyle(CardService.ImageStyle.CIRCLE);
    card.setHeader(header);

    // Section: Notebook Selection
    const section = CardService.newCardSection();

    // Get Notebooks (Hybrid: API + Live Drive Folders)
    const notebooks = getNotebooks();

    // Use a separate header to avoid Dropdown overlap issues
    section.addWidget(CardService.newTextParagraph().setText("<b>Select Target Notebook</b>"));

    const selectionInput = CardService.newSelectionInput()
        .setFieldName('notebook_id')
        .setType(CardService.SelectionInputType.DROPDOWN);

    // Default Option
    selectionInput.addItem('Default (Root Folder)', '', notebooks.length === 0);

    notebooks.forEach(nb => {
        // nb is { name: "Foo", id: "xyz" }
        selectionInput.addItem(nb.name, nb.id, false);
    });

    section.addWidget(selectionInput);

    if (notebooks.length === 0) {
        section.addWidget(CardService.newTextParagraph()
            .setText('<i>Tip: Go to Settings to create a Target Folder.</i>'));
    }

    // Section: Options
    const optionsSection = CardService.newCardSection();

    const checkboxSwitch = CardService.newSwitch()
        .setFieldName('include_attachments')
        .setValue('true')
        .setSelected(true);

    const checkbox = CardService.newDecoratedText()
        .setTopLabel('Options')
        .setText('Include Attachments')
        .setSwitchControl(checkboxSwitch);
    optionsSection.addWidget(checkbox);

    const action = CardService.newAction()
        .setFunctionName('onSaveClicked')
        .setLoadIndicator(CardService.LoadIndicator.SPINNER)
        .setParameters({ messageId: messageId });

    const button = CardService.newTextButton()
        .setText('Save to NotebookLM')
        .setOnClickAction(action)
        .setTextButtonStyle(CardService.TextButtonStyle.FILLED);

    optionsSection.addWidget(CardService.newButtonSet().addButton(button));

    const settingsAction = CardService.newAction().setFunctionName('onSettingsClicked');
    const settingsButton = CardService.newTextButton()
        .setText('⚙️ Settings')
        .setOnClickAction(settingsAction);
    optionsSection.addWidget(CardService.newButtonSet().addButton(settingsButton));

    card.addSection(section);
    card.addSection(optionsSection);
    return card.build();
}

/**
 * Helper to get the default Root Name if not set.
 */
function getDefaultRootName() {
    const email = Session.getActiveUser().getEmail();
    // Sanitize email slightly? 'NotebookLM_tim@augos.com' is fine for a folder name.
    return 'NotebookLM_' + email;
}

/**
 * Creates the settings card.
 */
function createSettingsCard() {
    const card = CardService.newCardBuilder()
        .setHeader(CardService.newCardHeader().setTitle('Settings'));

    const props = PropertiesService.getUserProperties();
    const gcpProject = props.getProperty('gcp_project') || '797532978992';
    const apiEnabled = props.getProperty('api_enabled') === 'true';
    const rootFolderName = props.getProperty('root_folder_name') || getDefaultRootName();

    // --- General Config ---
    const generalSection = CardService.newCardSection().setHeader('General Configuration');
    generalSection.addWidget(CardService.newTextInput()
        .setFieldName('root_folder_name')
        .setTitle('Root Drive Folder Name')
        .setValue(rootFolderName));

    generalSection.addWidget(CardService.newTextButton()
        .setText('Save Folder Name')
        .setOnClickAction(CardService.newAction().setFunctionName('onSaveGeneralConfig')));
    card.addSection(generalSection);

    // --- GCP Section ---
    const gcpSection = CardService.newCardSection().setHeader('Enterprise API (Optional)');

    const apiSwitch = CardService.newSwitch()
        .setFieldName('api_enabled')
        .setValue('true')
        .setSelected(apiEnabled)
        .setOnChangeAction(CardService.newAction().setFunctionName('onApiToggle'));

    gcpSection.addWidget(CardService.newDecoratedText()
        .setText('Enable GCP API')
        .setBottomLabel('Requires valid Project Number & API access')
        .setSwitchControl(apiSwitch));

    if (apiEnabled) {
        gcpSection.addWidget(CardService.newTextInput()
            .setFieldName('gcp_project')
            .setTitle('GCP Project Number')
            .setValue(gcpProject));

        gcpSection.addWidget(CardService.newTextButton()
            .setText('Save GCP Config')
            .setOnClickAction(CardService.newAction().setFunctionName('onSaveGcpConfig')));
    }
    card.addSection(gcpSection);

    // --- Drive Folders (Manual Targets) Section ---
    const manualSection = CardService.newCardSection().setHeader('Drive Targets (Clean & Instant)');

    manualSection.addWidget(CardService.newTextInput()
        .setFieldName('new_notebook_name')
        .setTitle('Create New Target Folder'));

    manualSection.addWidget(CardService.newTextButton()
        .setText('Create Folder')
        .setOnClickAction(CardService.newAction().setFunctionName('onAddNotebook')));

    // Live List Scanning
    const driveFolders = NotebookService.getSubfolders(rootFolderName);
    if (driveFolders.length > 0) {
        let folderNames = driveFolders.map(f => f.name).join(', ');
        if (folderNames.length > 200) folderNames = folderNames.substring(0, 200) + "...";

        manualSection.addWidget(CardService.newTextParagraph()
            .setText(`<b>Existing Targets:</b><br>${folderNames}`));
    } else {
        manualSection.addWidget(CardService.newTextParagraph().setText('No target folders found in Root.'));
    }

    // Back
    const backAction = CardService.newAction().setFunctionName('onBackClicked');
    manualSection.addWidget(CardService.newButtonSet()
        .addButton(CardService.newTextButton().setText('Back').setOnClickAction(backAction)));

    card.addSection(manualSection);
    return card.build();
}

/**
 * Handlers
 */
function onSettingsClicked(e) {
    return CardService.newActionResponseBuilder()
        .setNavigation(CardService.newNavigation().pushCard(createSettingsCard()))
        .build();
}

function onBackClicked(e) {
    return CardService.newActionResponseBuilder()
        .setNavigation(CardService.newNavigation().popCard())
        .build();
}

function onSaveGeneralConfig(e) {
    const rootName = e.formInput.root_folder_name;
    if (rootName) {
        PropertiesService.getUserProperties().setProperty('root_folder_name', rootName);
    }
    return CardService.newActionResponseBuilder()
        .setNotification(CardService.newNotification().setText("Saved Root Folder Name"))
        .build();
}

function onApiToggle(e) {
    const enabled = e.formInput.api_enabled === 'true';
    PropertiesService.getUserProperties().setProperty('api_enabled', enabled.toString());
    return CardService.newActionResponseBuilder()
        .setNavigation(CardService.newNavigation().updateCard(createSettingsCard()))
        .build();
}

function onSaveGcpConfig(e) {
    const project = e.formInput.gcp_project;
    PropertiesService.getUserProperties().setProperty('gcp_project', project);
    return CardService.newActionResponseBuilder()
        .setNotification(CardService.newNotification().setText("Saved Config"))
        .build();
}

function onAddNotebook(e) {
    const name = e.formInput.new_notebook_name;
    const props = PropertiesService.getUserProperties();
    const rootFolderName = props.getProperty('root_folder_name') || getDefaultRootName();

    if (name) {
        // This creates the folder in Drive immediately
        NotebookService.createSubfolder(name, rootFolderName);
    }

    // Refresh the card - this will fetch the new folder list immediately
    return CardService.newActionResponseBuilder()
        .setNotification(CardService.newNotification().setText(`Created Target: ${name}`))
        .setNavigation(CardService.newNavigation().updateCard(createSettingsCard()))
        .build();
}

function onSaveClicked(e) {
    const messageId = e.parameters.messageId;
    const includeAttachments = e.formInput.include_attachments === 'true';
    const notebookId = e.formInput.notebook_id;

    let notebookName = notebookId;
    const allNotebooks = getNotebooks();
    const match = allNotebooks.find(n => n.id === notebookId);
    if (match) notebookName = match.name;

    try {
        const props = PropertiesService.getUserProperties();
        const apiEnabled = props.getProperty('api_enabled') === 'true';
        const projectNumber = props.getProperty('gcp_project');
        const rootFolderName = props.getProperty('root_folder_name') || getDefaultRootName();

        let resultMsg = "";

        // 1. Try API Upload
        if (apiEnabled && projectNumber && notebookId && notebookId.startsWith('projects/')) {
            try {
                const apiResult = NotebookService.uploadToNotebookLM(projectNumber, notebookId, messageId);
                if (apiResult.success) resultMsg += "[API Upload Success] ";
            } catch (e) {
                console.error("API Upload Failed", e);
                resultMsg += "[API Failed, using Drive] ";
            }
        }

        // 2. Drive Save (Backup / Primary)
        // attachments are handled optionally inside saveEmailToDrive
        const result = NotebookService.saveEmailToDrive(messageId, includeAttachments, notebookName, rootFolderName);
        resultMsg += result.message;

        return CardService.newActionResponseBuilder()
            .setNotification(CardService.newNotification().setText(resultMsg).setType(CardService.NotificationType.INFO))
            .build();

    } catch (err) {
        return CardService.newActionResponseBuilder()
            .setNotification(CardService.newNotification().setText("Error: " + err.toString()))
            .build();
    }
}

/**
 * Homepage Trigger
 * Displayed when the user clicks the add-on icon but has no email open.
 */
function onHomepage(e) {
    return createHomepageCard();
}

/**
 * Creates the Batch Operations Card (Homepage)
 */
function createHomepageCard() {
    const card = CardService.newCardBuilder();

    // Header
    const header = CardService.newCardHeader()
        .setTitle('NotebookLM Batch Tools')
        .setSubtitle('Search & Save Multiple Threads')
        .setImageUrl('https://www.gstatic.com/images/icons/material/system/1x/library_books_black_24dp.png');
    card.setHeader(header);

    const section = CardService.newCardSection();

    // 1. Search Query
    section.addWidget(CardService.newTextInput()
        .setFieldName('batch_search_term')
        .setTitle('Gmail Search Query')
        .setHint('e.g. "from:Etana", "label:Work", "is:starred"')
        .setValue(''));

    // 2. Notebook Selection (Reuse Helper)
    const notebooks = getNotebooks();
    section.addWidget(CardService.newTextParagraph().setText("<b>Select Target Notebook</b>"));

    const selectionInput = CardService.newSelectionInput()
        .setFieldName('notebook_id')
        .setType(CardService.SelectionInputType.DROPDOWN);

    // Default Option
    selectionInput.addItem('Default (Root Folder)', '', notebooks.length === 0);
    notebooks.forEach(nb => selectionInput.addItem(nb.name, nb.id, false));

    section.addWidget(selectionInput);

    // 3. Action Buttons
    const previewAction = CardService.newAction().setFunctionName('onBatchPreview');
    section.addWidget(CardService.newTextButton()
        .setText('Preview Match Count')
        .setOnClickAction(previewAction)
        .setTextButtonStyle(CardService.TextButtonStyle.FILLED));

    card.addSection(section);

    // Settings Link
    const settingsSection = CardService.newCardSection();
    settingsSection.addWidget(CardService.newTextButton()
        .setText('⚙️ Settings')
        .setOnClickAction(CardService.newAction().setFunctionName('onSettingsClicked')));
    card.addSection(settingsSection);

    return card.build();
}

/**
 * Preview Handler: Shows matching threads with checkboxes.
 */
function onBatchPreview(e) {
    // Robust Input Retrieval
    let query = "";
    if (e.formInput && e.formInput.search_query) {
        query = e.formInput.search_query;
    } else if (e.formInputs && e.formInputs.search_query && e.formInputs.search_query[0]) {
        query = e.formInputs.search_query[0];
    } else if (e.formInput && e.formInput.batch_search_term) {
        query = e.formInput.batch_search_term;
    }

    // FIX: Safe access for notebook_id to prevent silent crash
    const notebookId = (e.formInput && e.formInput.notebook_id) || "";

    if (!query) {
        const debugDump = "Input: " + JSON.stringify(e.formInput || {}) + " || Inputs: " + JSON.stringify(e.formInputs || {});
        // Fallback or just empty
        return CardService.newActionResponseBuilder()
            .setNotification(CardService.newNotification().setText("Please enter a search query. Debug: " + debugDump))
            .build();
    }

    try {
        // Search Gmail (Limit 50 to prevent timeout)
        // We fetch 50 to give them options, but processing 50 PDFs might time out.
        const threads = GmailApp.search(query, 0, 50);
        const count = threads.length;

        const card = CardService.newCardBuilder()
            .setHeader(CardService.newCardHeader().setTitle(`Found ${count} Thread(s)`));

        const section = CardService.newCardSection();

        if (count === 0) {
            section.addWidget(CardService.newTextParagraph().setText(`No matching threads found for query: "<b>${query}</b>"`));
            section.addWidget(CardService.newTextParagraph().setText("<i>Try 'from:name', 'is:starred', or 'label:work'</i>"));

            // Debugging Info for User
            const debugInfo = Object.keys(e.formInput || {}).join(", ");
            section.addWidget(CardService.newTextParagraph().setText(`<i>Debug info (received inputs): ${debugInfo}</i>`));

            section.addWidget(CardService.newTextButton().setText("Back").setOnClickAction(CardService.newAction().setFunctionName('onHomepage')));
        } else {
            // --- SMART DASHBOARD START ---
            // Calculate Stats (Time & People) locally
            // Note: AnalysisService must be defined in the project files
            const stats = AnalysisService.calculateStats(threads);

            if (stats) {
                // 1. Timeline Section
                section.addWidget(CardService.newTextParagraph()
                    .setText(`<b>Activity (Last 30 Days)</b><br><font size="4" color="#4285F4">${stats.timelineSparkline}</font>`));

                // 2. People Section
                let peopleText = "<b>Top Senders:</b><br>";
                if (stats.topSenders.length > 0) {
                    peopleText += stats.topSenders.map(s => `• ${s.name} (${s.count})`).join("<br>");
                } else {
                    peopleText += "<i>No sender data found</i>";
                }
                section.addWidget(CardService.newTextParagraph().setText(peopleText));
            }
            // --- SMART DASHBOARD END ---

            section.addWidget(CardService.newDivider());

            section.addWidget(CardService.newTextParagraph()
                .setText(`Select threads to save to <b>${notebookId || 'Default'}</b>. <br><i>(Showing max 50 for performance)</i>`));

            // Checkbox List
            const checkboxGroup = CardService.newSelectionInput()
                .setFieldName('thread_selection')
                .setType(CardService.SelectionInputType.CHECK_BOX)
                .setTitle('Select Threads');

            threads.forEach(t => {
                const subject = t.getFirstMessageSubject() || "(No Subject)";
                const snippet = t.getLastMessageDate().toLocaleDateString(); // Simple date
                // Value is Thread ID
                checkboxGroup.addItem(`${subject} (${snippet})`, t.getId(), true);
            });

            section.addWidget(checkboxGroup);

            // Save Action
            const saveAction = CardService.newAction()
                .setFunctionName('onBatchSave')
                .setParameters({
                    notebookId: notebookId || ""
                });

            section.addWidget(CardService.newTextButton()
                .setText(`Save Selected`)
                .setOnClickAction(saveAction)
                .setTextButtonStyle(CardService.TextButtonStyle.FILLED));

            section.addWidget(CardService.newTextButton().setText("Cancel").setOnClickAction(CardService.newAction().setFunctionName('onHomepage')));
        }

        card.addSection(section);
        return CardService.newActionResponseBuilder()
            .setNavigation(CardService.newNavigation().pushCard(card.build()))
            .build();

    } catch (err) {
        console.error("Search Error: " + err);
        return CardService.newActionResponseBuilder()
            .setNotification(CardService.newNotification().setText("Search failed: " + err.toString()))
            .build();
    }
}

/**
 * Recursive Batch Save Handler
 */
function onBatchSave(e) {
    const CHUNK_SIZE = 5;

    let threadIds = [];
    let totalCount = 0;
    let processedCount = 0;
    let notebookId = "";
    let query = "";

    if (e.parameters && e.parameters.is_recursive === 'true') {
        threadIds = JSON.parse(e.parameters.remaining_ids);
        totalCount = parseInt(e.parameters.total_count);
        processedCount = parseInt(e.parameters.processed_count);
        notebookId = e.parameters.notebookId;
        query = e.parameters.query;
    } else {
        if (e.formInputs && e.formInputs.thread_selection) {
            threadIds = e.formInputs.thread_selection;
        }
        if (!threadIds || threadIds.length === 0) {
            return CardService.newActionResponseBuilder()
                .setNotification(CardService.newNotification().setText("No threads selected."))
                .build();
        }
        totalCount = threadIds.length;
        processedCount = 0;
        notebookId = e.parameters.notebookId;
        query = e.parameters.query;
    }

    const batch = threadIds.slice(0, CHUNK_SIZE);
    const remainingIds = threadIds.slice(CHUNK_SIZE);

    let notebookName = notebookId;
    const allNotebooks = getNotebooks();
    const match = allNotebooks.find(n => n.id === notebookId);
    if (match) notebookName = match.name;

    const props = PropertiesService.getUserProperties();
    const rootFolderName = props.getProperty('root_folder_name') || getDefaultRootName();

    // Track logs for this batch
    let recentLogs = [];

    batch.forEach(id => {
        try {
            const thread = GmailApp.getThreadById(id);
            const subject = thread.getFirstMessageSubject().substring(0, 40) + "..."; // Truncate for UI
            const firstMsgId = thread.getMessages()[0].getId();

            NotebookService.saveEmailToDrive(firstMsgId, true, notebookName, rootFolderName);
            recentLogs.push(`✅ ${subject}`);
        } catch (err) {
            console.error(err);
            recentLogs.push(`❌ (Error)`);
        }
    });

    processedCount += batch.length;
    const isFinished = remainingIds.length === 0;

    if (isFinished) {
        return createBatchResultCard(totalCount, processedCount, true);
    } else {
        // Pass logs to the progress card
        return createBatchProgressCard(remainingIds, totalCount, processedCount, notebookId, query, recentLogs);
    }
}

/**
 * Helper: Shows the "Continue" card with detailed logs.
 */
function createBatchProgressCard(remainingIds, total, processed, notebookId, query, recentLogs) {
    const card = CardService.newCardBuilder()
        .setHeader(CardService.newCardHeader().setTitle('Processing Batch...'));

    const section = CardService.newCardSection();

    const percentage = Math.round((processed / total) * 100);
    const bars = "🟩".repeat(Math.floor(percentage / 10)) + "⬜".repeat(10 - Math.floor(percentage / 10));

    section.addWidget(CardService.newTextParagraph()
        .setText(`<b>${percentage}% Complete</b><br>${bars}`));

    // Show Recent Files
    if (recentLogs && recentLogs.length > 0) {
        section.addWidget(CardService.newTextParagraph()
            .setText("<b>Just Saved:</b><br>" + recentLogs.join("<br>")));
    }

    section.addWidget(CardService.newTextParagraph()
        .setText(`<i>Ready for next ${Math.min(remainingIds.length, 5)}...</i>`));

    const continueAction = CardService.newAction()
        .setFunctionName('onBatchSave')
        .setParameters({
            is_recursive: 'true',
            remaining_ids: JSON.stringify(remainingIds),
            total_count: total.toString(),
            processed_count: processed.toString(),
            notebookId: notebookId || "",
            query: query || ""
        });

    section.addWidget(CardService.newTextButton()
        .setText('▶️ Continue Auto-Save')
        .setOnClickAction(continueAction)
        .setTextButtonStyle(CardService.TextButtonStyle.FILLED));

    card.addSection(section);
    return CardService.newActionResponseBuilder()
        .setNavigation(CardService.newNavigation().updateCard(card.build()))
        .build();
}

/**
 * Helper: Shows Final Result
 */
function createBatchResultCard(total, processed, completed) {
    const card = CardService.newCardBuilder()
        .setHeader(CardService.newCardHeader().setTitle('Batch Complete ✅'));

    const section = CardService.newCardSection();
    section.addWidget(CardService.newTextParagraph()
        .setText(`Successfully processed <b>${processed} / ${total}</b> threads.`));

    section.addWidget(CardService.newTextButton()
        .setText('Start New Search')
        .setOnClickAction(CardService.newAction().setFunctionName('onHomepage')));

    card.addSection(section);
    return CardService.newActionResponseBuilder()
        .setNavigation(CardService.newNavigation().updateCard(card.build()))
        .setNotification(CardService.newNotification().setText("Batch Complete"))
        .build();
}


/**
 * Data Helpers
 */
function getNotebooks() {
    const props = PropertiesService.getUserProperties();
    const apiEnabled = props.getProperty('api_enabled') === 'true';
    const projectNumber = props.getProperty('gcp_project');
    const rootFolderName = props.getProperty('root_folder_name') || getDefaultRootName();

    let list = [];

    // 1. API Results
    if (apiEnabled && projectNumber) {
        try {
            const apiNotebooks = NotebookService.fetchNotebooksFromApi(projectNumber);
            list = list.concat(apiNotebooks);
        } catch (e) {
            console.log('API List failed: ' + e);
        }
    }

    // 2. Live Drive Scan
    try {
        // This fetches real folders from Drive right now
        const driveFolders = NotebookService.getSubfolders(rootFolderName);
        driveFolders.forEach(df => {
            if (!list.find(item => item.id === df.id)) {
                list.push(df);
            }
        });
    } catch (e) {
        console.log('Drive List failed: ' + e);
    }

    return list;
}

/**
 * DEBUG FUNCTION
 * Run this from the Apps Script Editor toolbar to force Re-Authorization
 * and verify Drive permissions are working.
 */
function debugDriveAccess() {
    const email = Session.getActiveUser().getEmail();
    console.log("Current User: " + email);

    const rootName = getDefaultRootName();
    console.log("Attempting to access Drive Root: " + rootName);

    // This line triggers the permission check
    const folders = DriveApp.getFoldersByName(rootName);

    if (folders.hasNext()) {
        console.log("Success: Found existing root folder.");
    } else {
        console.log("Success: No folder found (but access is working). Attempting creation...");
        // Verify creation permission
        const newFolder = DriveApp.createFolder(rootName);
        console.log("Created folder: " + newFolder.getUrl());
    }
    console.log("All Permissions are VALID.");
}
