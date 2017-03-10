data "terraform_remote_state" "common" {
  backend = "local"

  config {
    path = "${path.module}/../common/terraform.tfstate"
  }
}

resource "google_dns_record_set" "stage" {
  managed_zone = "${data.terraform_remote_state.common.root_zone}"
  name         = "stage.yellottyellott.com."
  type         = "A"
  ttl          = 15
  rrdatas      = ["${google_compute_instance.stage.network_interface.0.access_config.0.assigned_nat_ip}"]
}
