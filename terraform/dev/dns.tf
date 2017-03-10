data "terraform_remote_state" "common" {
  backend = "local"

  config {
    path = "${path.module}/../common/terraform.tfstate"
  }
}

resource "google_dns_record_set" "dev" {
  managed_zone = "${data.terraform_remote_state.common.root_zone}"
  name         = "dev.yellottyellott.com."
  type         = "A"
  ttl          = 15
  rrdatas      = ["10.1.1.111"]
}
