# Deployment Instructions

Since this is a Google Apps Script project, you need to deploy it to your Google Workspace account.

## Option 1: Manual Copy-Paste (Easiest)

1.  Go to [script.google.com](https://script.google.com/) and create a **New Project**.
2.  Name it "Gmail to NotebookLM".
3.  **Project Settings**:
    - Click the gear icon (Project Settings).
    - Check the box "Show \"appsscript.json\" manifest file in editor".
4.  **Copy Files**:
    - Open `appsscript.json`: Paste content from local `appsscript.json`.
    - Open `Code.gs` (rename default): Paste content from local `Code.js`.
    - Create `NotebookService.gs`: Paste content from local `NotebookService.js`.
5.  **GCP Project Link (CRITICAL)**:
    - Go to **Project Settings** in Apps Script -> **Google Cloud Platform (GCP) Project**.
    - Click **Change Project**.
    - Enter Project Number: **`797532978992`** (augos-core-data).
    - *Note: Ensure the NotebookLM/Vertex AI API is enabled in this project.*
6.  **Deploy**:
    - Click **Deploy** -> **Test deployments**.
    - Select type: **Google Workspace Add-on**.
    - Click **Install**.
7.  **Test**:
    - Open your Gmail and look for the icon.

## Option 2: Using CLASP (Command Line)

1.  `clasp login`
2.  `clasp create --title "Gmail to NotebookLM" --type addon`
3.  `clasp push`
4.  `clasp deploy`

## Usage Guide

### Manual Mode
1.  Go to **Settings**.
2.  Add a Notebook Name.
3.  Select it in the dropdown and Save.

### Enterprise API Mode
1.  Go to **Settings**.
2.  Toggle "Enable GCP API".
3.  Your Project Number (**797532978992**) should be pre-filled.
4.  Click **Save GCP Config**.
5.  Go back. The dropdown should now try to fetch your actual notebooks.
