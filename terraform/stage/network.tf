resource "google_compute_network" "stage" {
  name                    = "stage"
  auto_create_subnetworks = "true"
}

resource "google_compute_firewall" "stage-icmp" {
  name          = "stage-icmp"
  network       = "${google_compute_network.stage.name}"
  source_ranges = ["0.0.0.0/0"]

  allow {
    protocol = "icmp"
  }
}

resource "google_compute_firewall" "stage-internal" {
  name          = "stage-internal"
  network       = "${google_compute_network.stage.name}"
  source_ranges = ["10.128.0.0/9"]

  allow {
    protocol = "icmp"
  }
}

resource "google_compute_firewall" "stage-web" {
  name          = "stage-web-public"
  network       = "${google_compute_network.stage.name}"
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
