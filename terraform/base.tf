terraform {
  required_version = "> 0.8.0"
}

provider "google" {
  credentials = "${file("../account.json")}"
  project     = "yellottyellott-com"
  region      = "us-central1"
}
