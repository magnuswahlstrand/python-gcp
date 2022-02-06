output "order-created-topic" {
  value = module.pubsub_order_created.topic
}

output "order-fulfilled-topic" {
  value = module.pubsub_order_fulfilled.topic
}
