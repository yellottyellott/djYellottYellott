data "terraform_remote_state" "common" {
  backend = "local"

  config {
    path = "${path.module}/../common/terraform.tfstate"
  }
}

resource "google_dns_record_set" "apex" {
  managed_zone = "${data.terraform_remote_state.common.root_zone}"
  name         = "yellottyellott.com."
  type         = "A"
  ttl          = 15
  rrdatas      = ["${google_compute_instance.prod.network_interface.0.access_config.0.assigned_nat_ip}"]
}

resource "google_dns_record_set" "www" {
  managed_zone = "${data.terraform_remote_state.common.root_zone}"
  name         = "www.yellottyellott.com."
  type         = "A"
  ttl          = 15
  rrdatas      = ["${google_compute_instance.prod.network_interface.0.access_config.0.assigned_nat_ip}"]
}

resource "google_dns_record_set" "mx" {
  managed_zone = "${data.terraform_remote_state.common.root_zone}"
  name         = "yellottyellott.com."
  type         = "MX"
  ttl          = 3600

  rrdatas = [
    "1 aspmx.l.google.com.",
    "5 alt1.aspmx.l.google.com.",
    "5 alt2.aspmx.l.google.com.",
    "10 alt3.aspmx.l.google.com.",
    "10 alt4.aspmx.l.google.com.",
  ]
}

resource "google_dns_record_set" "mail" {
  managed_zone = "${data.terraform_remote_state.common.root_zone}"
  name         = "mail.yellottyellott.com."
  type         = "CNAME"
  ttl          = 3600
  rrdatas      = ["ghs.googlehosted.com."]
}

resource "google_dns_record_set" "calendar" {
  managed_zone = "${data.terraform_remote_state.common.root_zone}"
  name         = "calendar.yellottyellott.com."
  type         = "CNAME"
  ttl          = 3600
  rrdatas      = ["ghs.googlehosted.com."]
}

resource "google_dns_record_set" "drive" {
  managed_zone = "${data.terraform_remote_state.common.root_zone}"
  name         = "drive.yellottyellott.com."
  type         = "CNAME"
  ttl          = 3600
  rrdatas      = ["ghs.googlehosted.com."]
}
