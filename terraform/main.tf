terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  token     = var.yc_token
  cloud_id  = var.yc_cloud_id
  folder_id = var.yc_folder_id
  zone      = "ru-central1-a"
}

resource "yandex_compute_instance" "vm" {
  name = "pupils-bachelor-vm"
  
  resources {
    cores  = 2
    memory = 2
  }
  
  boot_disk {
    initialize_params {
      image_id = "fd80bm0rh4rkepi8v3d4"
    }
  }
  
  network_interface {
    subnet_id = yandex_vpc_subnet.subnet.id
    nat       = true
  }
}

resource "yandex_vpc_network" "network" {
  name = "pupils-network"
}

resource "yandex_vpc_subnet" "subnet" {
  name       = "pupils-subnet"
  zone       = "ru-central1-a"
  network_id = yandex_vpc_network.network.id
  v4_cidr_blocks = ["10.10.0.0/24"]
}

output "ip" {
  value = yandex_compute_instance.vm.network_interface[0].nat_ip_address
}
