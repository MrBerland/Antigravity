/**
 * Service to handle interactions with Google Drive and content preparation for NotebookLM.
 */
const NotebookService = {
  FOLDER_NAME: "NotebookLM Imports",

  /**
   * Gets or creates the folder where we save emails.
   * If notebookName is provided, it gets/creates a subfolder.
   * Uses rootFolderName if provided, otherwise defaults.
   */
  getOrCreateFolder: function (notebookName, rootFolderName) {
    const rootName = rootFolderName || this.FOLDER_NAME;

    // 1. Get/Create Root Folder
    let rootFolder;
    const rootFolders = DriveApp.getFoldersByName(rootName);
    if (rootFolders.hasNext()) {
      rootFolder = rootFolders.next();
    } else {
      rootFolder = DriveApp.createFolder(rootName);
    }

    // 2. If no notebook name, return root
    if (!notebookName) return rootFolder;

    // 3. Get/Create Subfolder
    const subFolders = rootFolder.getFoldersByName(notebookName);
    if (subFolders.hasNext()) {
      return subFolders.next();
    } else {
      return rootFolder.createFolder(notebookName);
    }
  },

  /**
   * Gets a list of subfolders in the Root directory.
   * Returns: [{ name: "Folder A", id: "Folder A" }, ...]
   */
  getSubfolders: function (rootFolderName) {
    const rootName = rootFolderName || this.FOLDER_NAME;
    // Ensure root exists first
    const rootFolder = this.getOrCreateFolder(null, rootName);

    const list = [];
    const folders = rootFolder.getFolders();
    while (folders.hasNext()) {
      const folder = folders.next();
      list.push({
        name: folder.getName(),
        id: folder.getName() // For Drive folders, ID is name (for our logic)
      });
    }
    return list;
  },

  /**
   * Creates a new subfolder in the Root directory.
   */
  createSubfolder: function (name, rootFolderName) {
    const rootName = rootFolderName || this.FOLDER_NAME;
    const rootFolder = this.getOrCreateFolder(null, rootName);

    // Check if exists
    const existing = rootFolder.getFoldersByName(name);
    if (!existing.hasNext()) {
      rootFolder.createFolder(name);
    }
  },

  /**
   * Sanitizes a string to be safe for filenames.
   */
  sanitizeFilename: function (name) {
    return name.replace(/[^a-zA-Z0-9._-]/g, ' ').trim().substring(0, 100);
  },

  /**
   * Saves the FULL EMAIL THREAD as a PDF to the Root/Notebook folder.
   * Also saves attachments from ALL messages in the thread if requested.
   */
  saveEmailToDrive: function (messageId, includeAttachments, notebookName, rootFolderName) {
    try {
      const message = GmailApp.getMessageById(messageId);
      const thread = message.getThread();
      const messages = thread.getMessages(); // Returns array from oldest to newest
      const subject = thread.getFirstMessageSubject();

      const rootName = rootFolderName || this.FOLDER_NAME;
      const rootFolder = this.getOrCreateFolder(null, rootName);
      const targetFolder = notebookName ? this.getOrCreateFolder(notebookName, rootName) : rootFolder;

      // 1. Compile Full Thread HTML
      let combinedHtml = `
        <html>
          <head>
            <style>
              body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
              .email-container { border-bottom: 2px solid #eee; margin-bottom: 30px; padding-bottom: 20px; }
              .header { background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 15px; }
              .meta { color: #555; font-size: 0.9em; margin: 2px 0; }
              .body-content { line-height: 1.5; color: #333; }
              .subject-line { font-size: 1.4em; font-weight: bold; margin-bottom: 20px; border-bottom: 3px solid #333; padding-bottom: 10px; }
            </style>
          </head>
          <body>
            <div class="subject-line">${subject}</div>
      `;

      let attachmentsToSave = [];
      let attachmentNamesSpy = new Set(); // To de-duplicate files

      messages.forEach(msg => {
        const from = msg.getFrom();
        const to = msg.getTo();
        const date = msg.getDate();
        const body = msg.getBody(); // HTML body

        combinedHtml += `
          <div class="email-container">
            <div class="header">
              <div class="meta"><b>From:</b> ${from}</div>
              <div class="meta"><b>To:</b> ${to}</div>
              <div class="meta"><b>Date:</b> ${date}</div>
            </div>
            <div class="body-content">${body}</div>
          </div>
        `;

        // 2. Collect Attachments from each message
        if (includeAttachments) {
          const atts = msg.getAttachments();
          atts.forEach(att => {
            // Simple de-dupe by name + size
            const key = att.getName() + "_" + att.getSize();
            if (!attachmentNamesSpy.has(key)) {
              attachmentNamesSpy.add(key);
              attachmentsToSave.push(att);
            }
          });
        }
      });

      combinedHtml += `</body></html>`;

      // 3. Create Thread PDF
      const pdfBlob = Utilities.newBlob(combinedHtml, 'text/html')
        .getAs('application/pdf')
        .setName(this.sanitizeFilename(subject) + ".pdf");

      targetFolder.createFile(pdfBlob);

      // 4. Save Attachments
      let savedCount = 0;
      attachmentsToSave.forEach(att => {
        targetFolder.createFile(att);
        savedCount++;
      });

      return { success: true, message: `Saved Thread & ${savedCount} Attachments to "${targetFolder.getName()}"` };

    } catch (e) {
      console.error(e);
      throw e;
    }
  },

  /**
   * Fetches notebooks from the Enterprise API.
   */
  fetchNotebooksFromApi: function (projectNumber) {
    const url = `https://notebooklm.googleapis.com/v1beta1/projects/${projectNumber}/locations/us-central1/notebooks`;
    const token = ScriptApp.getOAuthToken();

    const options = {
      method: 'get',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      },
      muteHttpExceptions: true
    };

    const response = UrlFetchApp.fetch(url, options);
    if (response.getResponseCode() !== 200) {
      console.log(`API Error ${response.getResponseCode()}: ${response.getContentText()}`);
      return [];
    }

    const data = JSON.parse(response.getContentText());
    if (data.notebooks) {
      return data.notebooks.map(nb => ({
        name: nb.displayName,
        id: nb.name
      }));
    }
    return [];
  },

  /**
   * Uploads the email content directly to a Notebook via API.
   * Note: This currently only uploads the active message data for simplicity.
   * TODO: Upgrade this to support full thread if needed.
   */
  uploadToNotebookLM: function (projectNumber, notebookId, messageId) {
    const message = GmailApp.getMessageById(messageId);
    const subject = message.getSubject() || "No Subject";
    const body = message.getBody(); // HTML body

    const token = ScriptApp.getOAuthToken();
    const url = `https://notebooklm.googleapis.com/v1beta1/${notebookId}/sources:upload`;

    const payload = {
      source: {
        displayName: subject,
        textData: {
          text: body
        }
      }
    };

    const options = {
      method: 'post',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    };

    const response = UrlFetchApp.fetch(url, options);
    if (response.getResponseCode() !== 200) {
      throw new Error(`Upload Error ${response.getResponseCode()}: ${response.getContentText()}`);
    }
    return { success: true };
  }
};
