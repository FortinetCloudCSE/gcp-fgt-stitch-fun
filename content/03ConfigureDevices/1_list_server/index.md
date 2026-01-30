---
title: "Task 1 - Create Block List on Debian VM"
linkTitle: "List Server"
chapter: false
weight: 2
---

|                            |    |  
|----------------------------| ----|
| **Goal**                   | Prepare Debian VM as a list server|
| **Task**                   | Modify index.html with ip block list|
| **Verify task completion** | Blocked IP presented when curl issued|

### Create list server

FortiGuard provides and extensive list of known C&C servers and known malicious sites.  These can be applied as part of Intrusion Prevention and DNS policies.  For the purposes of this lab, we are not going to use those, as they change pretty much constantly and sometimes our Partners (like GCP) take exception to us calling real C&C servers for training labs.  Instead, we are going to create a block list on our Debian VM, and then call it as an external threat feed on FortiGate.  So that we can verify the functionality, we are going to use a well known ip (8.8.8.8) that answers icmp traffic, and is almost always reachable.

1. **Apache2**

As part of the terraform deployment for our environment, we installed and enabled Apache2.  We are now going to modify index.html such that it is just a list of IP Addresses.

* SSH to the Debian VM from **Compute Engine** > **VM instances**

* From the CLI, enter ``` cd /var/www/html ``` and then issue ``` ls ``` command.  You should see a file named index.html

* At the prompt, type ``` sudo rm index.html ```

* Now type ``` sudo nano index.html ```

* When the nano screen opens, type in ``` 8.8.8.8 ```

* Save the document by typing ``` ctrl + o ```.  At the bottom of the screen you will be prompted: "File Name to Write: index.html" hit enter to accept this.

* Exit the document by typing ``` ctrl + x ```

* Now issue the ``` curl localhost ``` command at the prompt.  You should see something like

```sh
student-04-e6938c5f38ce@a-debian-vm-mkq:/var/www/html$ curl localhost
8.8.8.8
student-04-e6938c5f38ce@a-debian-vm-mkq:/var/www/html$
```

### Move to the next task
