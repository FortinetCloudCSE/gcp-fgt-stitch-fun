# FGT-IP
output "fgt1_ip" {
  value = format("https://%s:8443", google_compute_address.compute_address["fgt1-static-ip"].address)
}

output "fgt2_ip" {
  value = format("https://%s:8443", google_compute_address.compute_address["fgt2-static-ip"].address)
}

output "nlb_ip" {
  value = google_compute_address.compute_address["elb-static-ip"].address
}

# Debian VM outputs
output "debian_vm_internal_ip" {
  value       = google_compute_address.compute_address["debian-vm-ip"].address
  description = "Internal IP address of the Debian VM"
}

output "debian_vm_name" {
  value       = google_compute_instance.compute_instance["debian_vm_instance"].name
  description = "Name of the Debian VM instance"
}

output "debian_vm_zone" {
  value       = google_compute_instance.compute_instance["debian_vm_instance"].zone
  description = "Zone where the Debian VM is deployed"
}

# FGT-Username
output "fgt_username" {
  value = var.fgt_username
}
# FGT-Password
output "fgt_password" {
  value = var.fgt_password
}