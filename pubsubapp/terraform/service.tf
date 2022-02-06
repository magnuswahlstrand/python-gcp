# Cloud Run service
resource "google_secret_manager_secret" "sentry_connection_string" {
  secret_id = "sentry_connection_string"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_iam_member" "secret-access" {
  secret_id = google_secret_manager_secret.sentry_connection_string.id
  role = "roles/secretmanager.secretAccessor"
  member = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
  depends_on = [
    google_secret_manager_secret.sentry_connection_string]
}

resource "google_cloud_run_service" "pubsubapp" {
  name = "pubsubapp"
  location = "europe-west1"

  template {
    spec {
      containers {
        image = "gcr.io/b32-demo-projects/pubsubapp"
        env {
          name = "SENTRY_CONNECTION_STRING"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.sentry_connection_string.secret_id
              key = "2"
            }
          }
        }
      }
    }
  }
  traffic {
    percent = 100
    latest_revision = true
  }
}
