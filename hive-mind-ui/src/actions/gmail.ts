'use server';

import { google } from 'googleapis';
import { JWT } from 'google-auth-library';

// Configuration
const SERVICE_ACCOUNT_FILE = process.env.GOOGLE_APPLICATION_CREDENTIALS;
const SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.labels', 'https://www.googleapis.com/auth/gmail.compose'];

export async function getGmailService(userEmail: string = 'tim@augos.io') {
    if (!SERVICE_ACCOUNT_FILE) {
        throw new Error('GOOGLE_APPLICATION_CREDENTIALS not set in environment');
    }

    // We need to use JWT (JSON Web Token) auth to support "subject" (impersonation)
    // The standard GoogleAuth or keys from file doesn't always expose .subject easily in all versions.
    // Using JWT directly from google-auth-library is reliable for DWD.

    // Load the key file content
    // In a real app, you might parse the JSON file or use keyFile path check
    // Here we let google-auth-library handle the file path via keyFile

    const auth = new JWT({
        keyFile: SERVICE_ACCOUNT_FILE,
        scopes: SCOPES,
        subject: userEmail, // THIS IS CRITICAL FOR IMPERSONATION
    });

    // Verify can authorize (optional, lazy is fine)
    // await auth.authorize();

    const gmail = google.gmail({ version: 'v1', auth });
    return gmail;
}

export async function getThread(threadId: string, userEmail: string = 'tim@augos.io') {
    console.log(`[getThread] Fetching thread: ${threadId} for ${userEmail}`);
    if (!threadId) throw new Error("getThread: threadId is required");
    const gmail = await getGmailService(userEmail);
    const res = await gmail.users.threads.get({
        userId: 'me',
        id: threadId,
        format: 'full',
    });
    return res.data;
}

export async function sendReply(threadId: string, messageId: string, subject: string, recipient: string, body: string, userEmail: string = 'tim@augos.io') {
    const gmail = await getGmailService(userEmail);

    // Construct RFC 2822 email
    const emailLines = [];
    emailLines.push(`To: ${recipient}`);
    emailLines.push(`Subject: ${subject.startsWith('Re:') ? subject : 'Re: ' + subject}`);
    emailLines.push(`In-Reply-To: ${messageId}`);
    emailLines.push(`References: ${messageId}`);
    emailLines.push('Content-Type: text/plain; charset="UTF-8"');
    emailLines.push('MIME-Version: 1.0');
    emailLines.push('');
    emailLines.push(body);

    const email = emailLines.join('\r\n');
    const encodedEmail = Buffer.from(email).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

    await gmail.users.messages.send({
        userId: 'me',
        requestBody: {
            raw: encodedEmail,
            threadId: threadId
        }
    });
}
