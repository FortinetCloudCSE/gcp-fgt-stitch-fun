
region = "us-central1"
zone   = "us-central1-a"
zone2  = "us-central1-b"

# VPC Networks will use default values from variables.tf
# Subnets will use default values from variables.tf

# Prefixed to all resources
prefix = "a"

# FortiGate image and instance type
# 7.4.7 BYOL is projects/fortigcp-project-001/global/images/fortinet-fgt-747-20250123-001-w-license
# 7.4.7 PAYG is projects/fortigcp-project-001/global/images/fortinet-fgtondemand-747-20250123-001-w-license
# 7.4.8 BYOL is projects/fortigcp-project-001/global/images/fortinet-fgt-748-20250529-001-w-license
# 7.4.8 PAYG is "projects/fortigcp-project-001/global/images/fortinet-fgtondemand-748-20250529-001-w-license"
fortigate_vm_image     = "projects/fortigcp-project-001/global/images/fortinet-fgtondemand-764-20250902-001-w-license"
fortigate_machine_type = "n2-standard-4"
fortigate_license_files = {
  fgt1_instance = { name = null }
  fgt2_instance = { name = null }
}
license_type = "payg" # can be byol, flex, or payg, make sure the license is correct for the sku
flex_tokens  = ["token1", "token2"]
admin_port   = 8443
fgt_password = "D3v0ps@1234!"

# Debian VM Configuration
debian_vm_machine_type = "e2-micro"
debian_vm_image        = "debian-cloud/debian-12"

