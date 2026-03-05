'use server';

import { getGmailService } from './gmail';
// import { addGovernanceRule } from './governance'; // Fallback?

// Helper to parse headers case-insensitively
function getHeader(headers: any[], name: string): string | null {
    const h = headers.find(
        (header) => header.name.toLowerCase() === name.toLowerCase()
    );
    return h ? h.value : null;
}

export async function unsubscribeSender(sender: string) {
    try {
        const gmail = await getGmailService();

        // 1. Find the latest email/message from this sender
        // We search specifically for this sender
        const query = `from:${sender}`;
        const res = await gmail.users.messages.list({
            userId: 'me',
            q: query,
            maxResults: 1,
        });

        const messages = res.data.messages;
        if (!messages || messages.length === 0) {
            return { success: false, message: 'No emails found from sender to unsubscribe from.' };
        }

        const msgId = messages[0].id;
        if (!msgId) return { success: false, message: 'Invalid message ID.' };

        // 2. Fetch headers
        const msg = await gmail.users.messages.get({
            userId: 'me',
            id: msgId,
            format: 'metadata', // We only need headers
        });

        const headers = msg.data.payload?.headers || [];
        const listUnsubscribe = getHeader(headers, 'List-Unsubscribe');
        const listUnsubscribePost = getHeader(headers, 'List-Unsubscribe-Post');

        if (!listUnsubscribe) {
            return { success: false, message: 'No List-Unsubscribe header found. Cannot auto-unsubscribe.' };
        }

        // 3. Process Header
        // Header format: <https://example.com/u>, <mailto:u@example.com>
        // We want to prioritize POST (One-Click) if supported

        let oneClickUrl: string | null = null;
        let mailto: string | null = null;

        // Parse the angle brackets <...>
        const matches = listUnsubscribe.match(/<([^>]+)>/g);
        const urls = matches ? matches.map(m => m.slice(1, -1)) : [];

        // Find HTTP and MAILTO
        for (const url of urls) {
            if (url.startsWith('http')) oneClickUrl = url;
            if (url.startsWith('mailto:')) mailto = url;
        }

        // STRATEGY 1: One-Click POST (RFC 8058)
        if (oneClickUrl && listUnsubscribePost && listUnsubscribePost.includes('List-Unsubscribe=One-Click')) {
            console.log(`Unsubscribe Agent: Attempting One-Click POST to ${oneClickUrl}`);

            // We handle the POST request
            const response = await fetch(oneClickUrl, {
                method: 'POST',
                body: 'List-Unsubscribe=One-Click',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            });

            if (response.ok) {
                return { success: true, message: 'Successfully unsubscribed via One-Click POST.' };
            } else {
                console.warn(`One-Click POST failed: ${response.status} ${response.statusText}`);
                // Fallthrough to mailto if available
            }
        }

        // STRATEGY 2: Mailto
        if (mailto) {
            console.log(`Unsubscribe Agent: Sending email to ${mailto}`);
            const mailtoParts = mailto.replace('mailto:', '');
            const [toEmail, queryString] = mailtoParts.split('?');

            let subject = 'Unsubscribe';
            let body = 'Please unsubscribe me.';

            // Sometimes headers have ?subject=...
            if (queryString) {
                const params = new URLSearchParams(queryString);
                if (params.get('subject')) subject = params.get('subject')!;
                if (params.get('body')) body = params.get('body')!;
            }

            // Send Email
            // Construct raw email
            const messageParts = [
                `To: ${toEmail}`,
                'Content-Type: text/plain; charset="utf-8"',
                'MIME-Version: 1.0',
                `Subject: ${subject}`,
                '',
                body
            ];
            const rawMessage = messageParts.join('\n');
            const encodedMessage = Buffer.from(rawMessage).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

            await gmail.users.messages.send({
                userId: 'me',
                requestBody: {
                    raw: encodedMessage,
                },
            });

            return { success: true, message: `Sent unsubscribe request to ${toEmail}` };
        }

        // STRATEGY 3: Standard HTTP GET (Fallback/Click)
        // If we have a URL but no One-Click POST support, we can try GET, but usually this opens a landing page.
        // It's risky to auto-click links that might just confirm "Active User".
        // Safer to say "Click Required" or actually try it if the user wants "Aggressive Mode".
        // For now, let's report it.

        if (oneClickUrl) {
            return { success: false, message: 'Manual click required. Agent stopped (Safety).' };
        }

        return { success: false, message: 'Could not determine unsubscribe action.' };

    } catch (error: any) {
        console.error('Unsubscribe Agent Error:', error);
        return { success: false, message: `Agent Error: ${error.message}` };
    }
}
