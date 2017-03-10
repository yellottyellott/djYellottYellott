resource "google_compute_instance" "prod" {
  name         = "gyarados"
  machine_type = "f1-micro"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-1604-lts"
    }
  }

  network_interface {
    network = "${google_compute_network.prod.name}"

    access_config {
      // ephemeral IP
    }
  }

  # determines firewall rules
  tags = ["web-public"]
}
