terraform {
  backend "gcs" {
    bucket = "terraform-state-pubsub-app"
  }
}

locals {
  project_id = "b32-demo-projects"
}

provider "google" {
  project = local.project_id
}


resource "google_cloud_run_service" "pubsubapp" {
  name = "pubsubapp"
  location = "europe-west1"

  template {
    spec {
      containers {
        image = "gcr.io/b32-demo-projects/pubsubapp"
      }
    }
  }

  traffic {
    percent = 100
    latest_revision = true
  }
}


module "pubsub-dlq" {
  source = "terraform-google-modules/pubsub/google"
  project_id = local.project_id
  version = "~> v3.1"

  topic = "pubsubapp-dlq-topic"
  pull_subscriptions = [
    {
      name = "pull-dlq"
    }
  ]
}

module "pubsub" {
  source = "terraform-google-modules/pubsub/google"
  project_id = local.project_id
  version = "~> v3.1"

  topic = "pubsubapp-topic"
  push_subscriptions = [
    {
      name = "pubsubpush"
      push_endpoint = google_cloud_run_service.pubsubapp.status.0.url
      dead_letter_topic = module.pubsub-dlq.id
      max_delivery_attempts = 5
    }
  ]
}

output "cloud-run-url" {
  value = module.pubsub-dlq.id
}
