# -------------------------
# Диски
# -------------------------
resource "yandex_compute_disk" "boot-disk" {
  for_each = var.virtual_machines

  name     = each.value.disk_name
  type     = "network-hdd"
  zone     = var.zone
  size     = each.value.disk
  image_id = each.value.template
}

# -------------------------
# Берём существующую подсеть
# -------------------------
data "yandex_vpc_subnet" "sysadmin_subnet" {
  name      = "sysadmin-curse-network-subnet1"
  folder_id = var.folder_id
}

# -------------------------
# Виртуальные машины
# -------------------------
resource "yandex_compute_instance" "virtual_machine" {
  for_each = var.virtual_machines

  name        = each.value.vm_name
  description = each.value.vm_desc
  zone        = var.zone

  resources {
    cores  = each.value.vm_cpu
    memory = each.value.ram
  }

  boot_disk {
    disk_id = yandex_compute_disk.boot-disk[each.key].id
  }

  network_interface {
    subnet_id = data.yandex_vpc_subnet.sysadmin_subnet.id
    nat       = true
  }

  # Требование задания: доступ по SSH по ключу
  metadata = {
    ssh-keys = "${var.vm_user}:${file(var.ssh_public_key_path)}"
  }
}

