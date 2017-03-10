resource "google_compute_network" "prod" {
  name                    = "prod"
  auto_create_subnetworks = "true"
}

resource "google_compute_firewall" "prod-icmp" {
  name          = "prod-icmp"
  network       = "${google_compute_network.prod.name}"
  source_ranges = ["0.0.0.0/0"]

  allow {
    protocol = "icmp"
  }
}

resource "google_compute_firewall" "prod-internal" {
  name          = "prod-internal"
  network       = "${google_compute_network.prod.name}"
  source_ranges = ["10.128.0.0/9"]

  allow {
    protocol = "icmp"
  }
}

resource "google_compute_firewall" "prod-web" {
  name          = "prod-web-public"
  network       = "${google_compute_network.prod.name}"
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["web-public"]

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
}
