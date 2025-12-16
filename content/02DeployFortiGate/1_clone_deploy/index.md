---
title: "Task 1 - Clone and deploy the Github Repo"
linkTitle: "Clone and Deploy"
weight: 10
---

### Clone Github Repository and deploy resources

1. Open cloud shell

* On the top right hand side of the screen, click on the cursor icon.
* Several pop-ups will be created. When prompted, click Authorize.

  {{< figure src="open_shell.png" alt="open_shell" >}}

* The result should be a Cloud Shell at the bottom of the screen.

1. Clone the repo

* At the prrompt, enter ``` git clone https://github.com/FortinetCloudCSE/gcp-fgt-stitch-fun.git ```

  {{< figure src="clone1.png" alt="clone1" >}}

1. Deploy resources
  
* Navigate to the FortiGate deployment directory by typing ``` cd gcp-fgt-stitch-fun/terraform/gcp-fgt-a-p-new ```

* At the prompt issue the ``` terraform init ``` command.  You should get a message stating **Terraform has been successfully initialized!**

* For this next step, you will need to input your GCP project ID.  Conveniently, this is displayed right next to the prompt.  You can either use ``` ctrl + c ``` or ``` cmd + c ``` to copy the Project ID.

  {{< figure src="proj-id.png" alt="proj-id" >}}

* Now issue the ``` terraform apply --auto-approve ``` command.

* You will be prompted to "Enter a value:" for **var.project**.  Use ``` ctrl + v ``` or ``` cmd + v ``` and then it enter.

* The deployment will take some time to complete.  Take note of the outputs scrolling on the screen.

* There will be a number of outputs at the bottom of the screen.  For example:

```sh

debian_vm_internal_ip = "10.0.2.2"
debian_vm_name = "a-debian-vm-cbh"
debian_vm_zone = "us-central1-a"
fgt1_ip = "https://34.63.120.49:8443"
fgt2_ip = "https://34.28.104.25:8443"
fgt_password = "D3v0ps@1234!"
fgt_username = ""
nlb_ip = "130.211.212.222"

```

1. Verify FortiGate

* Click on the links from the output for fgt1_ip and fgt2_ip.  These are the dedicated management IP Addresses assigned to port4 on the FortiGate.  If the FortiGates aren't available, for a couple of minutes, they may still be bootstrapping.

* Log into FortiGates with username: ``` admin ``` and password ``` D3v0ps@1234! ```.  

* Check to ensure that HA status is synchronized by navigating to **System** > **HA**. If they are not synchronized, give them a couple of minutes.

* Next Navigate to **Security Fabric** > **External Connectors**. 

* Ensure that the GCP connector is up and hover over the icon to ensure that there are filters present

  {{< figure src="con-up.png" alt="con-up" >}}

1. Verify Debian VM

* In the Google Cloud Console, click on the "hamburger menu at the top left of the screen.

* Navigate to **Compute Engine** > **VM instances** and select the debian VM to go to the Details screen.

* Click on SSH.  This will open a new tab or pop-up with the cli for your debian device.

  {{< figure src="ssh-deb.png" alt="ssh-deb" >}}