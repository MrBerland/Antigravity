provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Enable Required APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "gmail.googleapis.com",
    "pubsub.googleapis.com",
    "cloudfunctions.googleapis.com",
    "run.googleapis.com",
    "bigquery.googleapis.com",
    "artifactregistry.googleapis.com"
  ])
  service = each.key
  disable_on_destroy = false
}

# 2. Pub/Sub Topic for Gmail Notifications
resource "google_pubsub_topic" "gmail_ingest" {
  name = "gmail-ingest-topic"
}

# Allow Gmail to publish to this topic
resource "google_pubsub_topic_iam_binding" "gmail_publish" {
  topic = google_pubsub_topic.gmail_ingest.name
  role  = "roles/pubsub.publisher"
  members = [
    "serviceAccount:gmail-api-push@system.gserviceaccount.com",
  ]
}

# 3. GCS Bucket for Raw JSON Storage (Data Lake)
resource "google_storage_bucket" "raw_email_lake" {
  name          = "${var.project_id}-raw-email-lake"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type = "Delete"
    }
  }
}

# 4. BigQuery Dataset & Table (Structured Data)
resource "google_bigquery_dataset" "hive_mind" {
  dataset_id = "hive_mind_core"
  location   = "US"
}

resource "google_bigquery_table" "messages" {
  dataset_id = google_bigquery_dataset.hive_mind.dataset_id
  table_id   = "messages"

  schema = <<EOF
[
  {
    "name": "message_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "thread_id",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "timestamp",
    "type": "TIMESTAMP",
    "mode": "NULLABLE"
  },
  {
    "name": "sender",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "subject",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "snippet",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "gcs_uri",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
}

# 5. Cloud Function (The Extractor)
resource "google_storage_bucket" "function_source" {
  name = "${var.project_id}-function-source"
  location = "US"
}

resource "google_storage_bucket_object" "source_zip" {
  name   = "source.zip"
  bucket = google_storage_bucket.function_source.name
  source = data.archive_file.function_zip.output_path
}

data "archive_file" "function_zip" {
    type        = "zip"
    source_dir  = "../src/extractor"
    output_path = "/tmp/extractor.zip"
}

resource "google_cloudfunctions_function" "extractor" {
  name        = "hive-mind-extractor"
  description = "Ingests Gmail Pub/Sub events"
  runtime     = "python310"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.function_source.name
  source_archive_object = google_storage_bucket_object.source_zip.name
  
  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.gmail_ingest.name
  }

  environment_variables = {
    PROJECT_ID = var.project_id
    BUCKET_NAME = google_storage_bucket.raw_email_lake.name
    DATASET_ID = google_bigquery_dataset.hive_mind.dataset_id
    TABLE_ID = google_bigquery_table.messages.table_id
  }
}

# 6. BigQuery Connection to Vertex AI (The "Brain" Link)
resource "google_bigquery_connection" "vertex_conn" {
  connection_id = "vertex_conn"
  project       = var.project_id
  location      = "US"
  cloud_resource {}
}

# Grant the BigQuery Connection SA access to Vertex AI
resource "google_project_iam_member" "vertex_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_bigquery_connection.vertex_conn.cloud_resource[0].service_account_id}"
}
