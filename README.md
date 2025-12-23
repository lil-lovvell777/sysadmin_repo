example repa
from cloud
Ansible and terraform projects have been added.
Terraform deploys 3 VMs, and Ansible manages them, namely, it sets up 2 VMs with webpages, and one vm proxies these 2 vms using nginx.
For Terraform, you need to configure your key.json for working with YC, and tfvars with their own data, and for ansible their own inventory.yaml
