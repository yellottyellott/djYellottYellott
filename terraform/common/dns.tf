resource "google_dns_managed_zone" "yellottyellott" {
  name     = "yellottyellott"
  dns_name = "yellottyellott.com."
}

output "root_zone" {
  value = "${google_dns_managed_zone.yellottyellott.name}"
}

output "root_zone_name_servers" {
  value = "${google_dns_managed_zone.yellottyellott.name_servers}"
}
