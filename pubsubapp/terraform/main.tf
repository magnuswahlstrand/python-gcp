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

data "google_project" "project" {
}

# Service accounts and IAM
resource "google_service_account" "pubsub_sa" {
  account_id = "pubsubapp-topic-sa"
  display_name = "A service account that only Jane can interact with"
}

resource "google_cloud_run_service_iam_binding" "binding" {
  location = google_cloud_run_service.pubsubapp.location
  project = google_cloud_run_service.pubsubapp.project
  service = google_cloud_run_service.pubsubapp.name
  role = "roles/run.invoker"
  members = [
    "serviceAccount:${google_service_account.pubsub_sa.email}",
  ]
}

resource "google_project_iam_binding" "project" {
  project = local.project_id
  role = "roles/iam.serviceAccountTokenCreator"

  members = [
    "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com",
  ]
}

# PubSub topics and subscriptions
module "pubsub_order_created" {
  source = "./modules/pubsub-with-dlq"

  project_id = local.project_id
  prefix = "order_created"
  push_endpoint = "${google_cloud_run_service.pubsubapp.status.0.url}/order/created"
  service_account_email = google_service_account.pubsub_sa.email
}

module "pubsub_order_fulfilled" {
  source = "./modules/pubsub-with-dlq"

  project_id = local.project_id
  prefix = "order_fulfilled"
  push_endpoint = "${google_cloud_run_service.pubsubapp.status.0.url}/order/fulfilled"
  service_account_email = google_service_account.pubsub_sa.email
}

