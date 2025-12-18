---
title: "Task 1 - Create Firewall Rule to Block Compromised Host "
linkTitle: "Firewall Rule"
chapter: false
weight: 2
---

|                            |    |  
|----------------------------| ----|
| **Goal**                   | Add firewall rule to GCP|
| **Task**                   | Configure VPC firewall rule in Google Cloud console|
| **Verify task completion** | Rule is present and confgired properly|

### Create firewall rule

We will modify the trust VPC firewall rules in GCP to block traffic from devices with a Network Tag named "compromised"

1. **Configure Rule**

* From the Google Cloud Console, navigate to **VPC Network** > **VPC networks**

* Select the **trust-vpc** to view VPC network details

* On the Firewalls Tab, scroll to Firewall Rules and click on **Create VPC firewall rule**

* Configure the rule as below and click on **Create**

  {{< figure src="gcp-fw.png" alt="gcp-f2" >}}

* Ensure that the new rule is now in the list

  {{< figure src="rules.png" alt="rules" >}}

### Move to the next task
