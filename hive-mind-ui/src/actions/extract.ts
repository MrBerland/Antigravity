'use server';

import { VertexAI } from '@google-cloud/vertexai';
import { getGmailService } from './gmail';

// Config
const PROJECT_ID = 'augos-core-data';
const LOCATION = 'us-central1';
const MODEL = 'gemini-2.0-flash-exp'; // SOTA speed/quality

// Initialize Vertex
const vertexAI = new VertexAI({ project: PROJECT_ID, location: LOCATION });

export async function extractEntities(messageId: string) {
    try {
        // 1. Fetch Email Content
        const gmail = await getGmailService();
        const msg = await gmail.users.messages.get({
            userId: 'me',
            id: messageId,
            format: 'full', // We need text
        });

        const snippet = msg.data.snippet;
        const headers = msg.data.payload?.headers;
        const subject = headers?.find(h => h.name === 'Subject')?.value || '';
        const sender = headers?.find(h => h.name === 'From')?.value || '';

        // TODO: Parse full body if snippet is insufficient. For MVP, snippet + subject is often enough.

        // 2. Call Gemini
        const generativeModel = vertexAI.preview.getGenerativeModel({
            model: MODEL,
            generationConfig: { responseMimeType: 'application/json' }
        });

        const prompt = `
    Analyze this email context from the "Hive Mind" corporate database.
    
    Task 1: Identify generic BUSINESS ENTITIES (Companies, Specific Sites, Assets, Ticket Numbers, Project Names).
    Task 2: PERFORM A PROCUREMENT ANALYSIS if applicable.
       - Look for energy/service proposals.
       - Group analysis ON A PER SITE BASIS.
       - For each site, extract and analyze EACH TENURE OPTION (e.g. 5-year, 10-year, 20-year terms).
       - Extract financials (savings, rates) for each tenure option.

    Context:
    From: ${sender}
    Subject: ${subject}
    Content: ${snippet}

    Return JSON:
    {
      "entities": [
        {
           "name": "Name of entity",
           "type": "COMPANY" | "SITE" | "ASSET" | "PROJECT" | "PERSON",
           "confidence": 0.0 to 1.0,
           "reason": "Why you extracted this"
        }
      ],
      "procurement_analysis": {
          "is_relevant": boolean,
          "sites": [
              {
                  "site_name": "Name of the site/facility",
                  "address": "Address if available",
                  "tenure_options": [
                      {
                          "duration": "e.g. 10 Years",
                          "savings_estimate": "e.g. R450,000 / year",
                          "rate": "e.g. 110c/kWh",
                          "escalation": "e.g. CPI + 1%",
                          "pros": ["list of pros"],
                          "cons": ["list of cons"]
                      }
                  ]
              }
          ]
      }
    }
    `;

        const resp = await generativeModel.generateContent(prompt);
        const content = resp.response.candidates?.[0]?.content?.parts?.[0]?.text;

        if (!content) throw new Error('No content from Gemini');

        return JSON.parse(content);

    } catch (error: any) {
        console.error('Entity Extraction Error:', error);
        return { error: error.message };
    }
}
