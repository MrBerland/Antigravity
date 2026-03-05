from google.cloud import bigquery
import os

PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE
client = bigquery.Client(project=PROJECT_ID)

print("--- DEBUG RAW LLM OUTPUT ---")
# Check the raw AI results directly (joining back to find the raw string)
# The `fact_work_patterns` table store the parsed values (which are null).
# We need to re-run a small prediction to see the RAW output string.

query_debug = """
SELECT 
    ml_generate_text_llm_result
FROM
    ML.GENERATE_TEXT(
      MODEL `hive_mind_core.gemini_flash`, 
      (
        SELECT 'Define the category of this work: "Writing SQL code"' as prompt
      ),
      STRUCT(
        0.0 AS temperature, 
        TRUE AS flatten_json_output
      )
    )
"""

try:
    rows = list(client.query(query_debug).result())
    print(f"Raw Output: {rows[0].ml_generate_text_llm_result}")
except Exception as e:
    print(f"Error: {e}")
