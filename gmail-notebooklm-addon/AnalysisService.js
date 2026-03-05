/**
 * Service for analyzing Gmail threads to generate dashboard stats.
 * Does not require external APIs.
 */
var AnalysisService = (function () {

    /**
     * analyzing a list of GmailThreads to extract stats.
     * @param {GmailThread[]} threads 
     * @returns {Object} { timeline: [], senders: [], categories: [] }
     */
    function calculateStats(threads) {
        if (!threads || threads.length === 0) return null;

        const senderCounts = {};
        const dateCounts = {};
        const now = new Date();

        // simple bucket for dates (YYYY-MM-DD)
        // using "Days ago" for the timeline bucket
        const bucketSize = 24 * 60 * 60 * 1000; // 1 day

        threads.forEach(t => {
            // 1. Sender Analysis
            // We use the last message to get the most recent activity contact
            // Or usually "From" of the first message is the initiator. 
            // Let's use the Messages array if possible, but fetching all messages is expensive.
            // GmailThread.getMessages() triggers a fetch. limiting to 50 threads * ~3 msgs = 150 fetches. 
            // Might be slow.
            // Optimization: Use `t.getMessages()[0]` only? 
            // Actually, `t.getMessages()` fetches the data. `t.getLastMessageDate()` is free.
            // `t.getMessages()` is cost-heavy. 
            // Let's see if we can get sender from search? No.
            // We MUST fetch messages to get the "From" header.
            // To be safe, we only analyze the *first* message of each thread for the "Initiator".

            const msgs = t.getMessages();
            if (msgs.length > 0) {
                const firstMsg = msgs[0];
                const fromRaw = firstMsg.getFrom();
                // Parse "Name <email@domain.com>" -> "Name"
                const nameMatch = fromRaw.match(/^"?([^"<]+)"?\s*</);
                let name = nameMatch ? nameMatch[1].trim() : fromRaw;
                if (name.includes('@')) name = name.split('@')[0]; // Fallback for raw emails

                // Sanitize
                name = name.replace(/"/g, '');

                senderCounts[name] = (senderCounts[name] || 0) + 1;
            }

            // 2. Timeline Analysis
            const date = t.getLastMessageDate();
            // Bucket by "Days Ago"
            const daysAgo = Math.floor((now - date) / bucketSize);
            if (daysAgo <= 30) { // Only track last 30 days
                dateCounts[daysAgo] = (dateCounts[daysAgo] || 0) + 1;
            }
        });

        // Format Timeline (Sparkline Logic)
        // Array of 30 days, value is count.
        const timeline = [];
        for (let i = 29; i >= 0; i--) {
            timeline.push(dateCounts[i] || 0);
        }

        // Top Senders
        const sortedSenders = Object.keys(senderCounts)
            .map(name => ({ name: name, count: senderCounts[name] }))
            .sort((a, b) => b.count - a.count)
            .slice(0, 5); // Top 5

        return {
            timeline: timeline,
            timelineSparkline: generateSparkline(timeline),
            topSenders: sortedSenders,
            totalAnalyzed: threads.length
        };
    }

    /**
     * Generates a unicode sparkline from an array of numbers.
     * Uses blocks:  ▂▃▄▅▆▇█
     */
    function generateSparkline(data) {
        const max = Math.max(...data);
        if (max === 0) return "______________________________";

        const levels = [" ", "▂", "▃", "▄", "▅", "▆", "▇", "█"];
        return data.map(val => {
            if (val === 0) return " ";
            const index = Math.min(levels.length - 1, Math.floor((val / max) * (levels.length - 1)));
            return levels[index];
        }).join("");
    }

    return {
        calculateStats: calculateStats
    };

})();
