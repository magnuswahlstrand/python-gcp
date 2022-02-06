variable "prefix" {
  description = "Prefix of resource"
  type = string
}

variable "project_id" {
  description = "GCP project ID"
  type = string
}

variable "push_endpoint" {
  description = "Service URL for PubSub push"
  type = string
}

variable "service_account_email" {
  description = "Service account used for pushing messages"
  type = string
}
