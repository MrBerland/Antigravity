import { BigQuery } from '@google-cloud/bigquery';
import path from 'path';

// Singleton instance
let bigqueryInstance: BigQuery | null = null;

export function getBigQueryClient() {
    if (!bigqueryInstance) {
        const options: any = {
            projectId: 'augos-core-data',
        };

        // Explicitly check for the known credentials file if not in Env
        const knownPath = '/Users/timstevens/Antigravity/HiveMind/credentials/hive-mind-admin.json';
        if (!process.env.GOOGLE_APPLICATION_CREDENTIALS && knownPath) {
            console.log("⚠️ GOOGLE_APPLICATION_CREDENTIALS not set. Using hardcoded path:", knownPath);
            options.keyFilename = knownPath;
        }

        bigqueryInstance = new BigQuery(options);
    }
    return bigqueryInstance;
}
