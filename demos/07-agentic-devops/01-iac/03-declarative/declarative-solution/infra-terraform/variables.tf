variable "environment_name" {
  description = "Name of the azd environment; becomes the azd-env-name tag and the resource group suffix."
  type        = string
}

variable "location" {
  description = "Azure region for every resource in this configuration."
  type        = string
  default     = "westeurope"
}

variable "sku_tier" {
  description = "Static Web App tier. Free is enough for the food-shop frontend."
  type        = string
  default     = "Free"
}
