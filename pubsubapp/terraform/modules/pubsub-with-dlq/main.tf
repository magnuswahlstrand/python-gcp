module "pubsub-dlq" {
  source = "terraform-google-modules/pubsub/google"
  project_id = var.project_id
  version = "~> v3.1"

  topic = "${var.prefix}_dlq"
  pull_subscriptions = [
    {
      name = "${var.prefix}_dlq_sub"
    }
  ]
}

module "pubsub-main" {
  source = "terraform-google-modules/pubsub/google"
  project_id = var.project_id
  version = "~> v3.1"

  topic = "${var.prefix}_main"
  push_subscriptions = [
    {
      name = "${var.prefix}_main_sub"
      push_endpoint = var.push_endpoint
      dead_letter_topic = module.pubsub-dlq.id
      max_delivery_attempts = 5
      oidc_service_account_email = var.service_account_email
    }
  ]
}
