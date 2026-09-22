output "AZURE_LOCATION" {
  value = azurerm_resource_group.main.location
}

output "RESOURCE_GROUP_NAME" {
  value = azurerm_resource_group.main.name
}

output "SERVICE_FOOD_SHOP_URI" {
  value = "https://${azurerm_static_web_app.food_shop.default_host_name}"
}
