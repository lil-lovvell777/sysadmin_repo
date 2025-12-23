variable "virtual_machines" {
  description = "VM definitions"
  type = map(object({
    vm_name   = string
    vm_desc   = string
    vm_cpu    = number
    ram       = number
    disk      = number
    disk_name = string
    template  = string
  }))
}

variable "sa_key_file" {
  type        = string
  description = "/home/top_sysadmin/terraform_yandex/key.json"
}

variable "cloud_id" {
  type = string
}

variable "folder_id" {
  type = string
}

variable "zone" {
  type    = string
  default = "ru-central1-b"
}

variable "subnet_id" {
  type        = string
  description = "Existing subnet ID where VMs will be created"
}

variable "vm_user" {
  type        = string
  description = "Linux user for SSH access"
  default     = "top_sysadmin"
}

variable "ssh_public_key_path" {
  type        = string
  description = "Path to SSH public key"
  default     = "~/.ssh/id_ed25519.pub"
}
