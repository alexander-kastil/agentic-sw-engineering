locals {
  resource_token = substr(lower(replace(uuidv5("dns", "${var.environment_name}.${var.location}"), "-", "")), 0, 13)

  tags = {
    "azd-env-name" = var.environment_name
  }
}

resource "azurerm_resource_group" "main" {
  name     = "rg-${var.environment_name}"
  location = var.location
  tags     = local.tags
}

resource "azurerm_static_web_app" "food_shop" {
  name                = "stapp-${local.resource_token}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku_tier            = var.sku_tier
  sku_size            = var.sku_tier

  tags = merge(local.tags, {
    "azd-service-name" = "food-shop"
  })
}
