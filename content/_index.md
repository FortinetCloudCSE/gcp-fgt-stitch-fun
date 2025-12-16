---
title: "Fortinet TECWorkshop Template - MVP2"
linkTitle: "TECWorkshop Template"
weight: 1
archetype: "home"
description: "Hugo for Fortinet TEC Workshops"
---

### FYI, YOU WILL NOW NEED TO CHECKIN WITH YOUR EMAIL ADDRESS TO VIEW THIS GUIDE
This change helps with analytics and data gathering and is consistent with UserRepo guide (this repo) serving as the root of every new workshop (e.g. this guide is always on latest and greatest featureset which gets cloned into every new workshop)  

### Lab Summary

This lab will explain how to use the FortiGate automation stitch integration with GCP cloud functions in order to automatically remediate security events.  We will configure an Active/Passive High Availability pair of FortiGate VMs in a Security Services Hub configuration. The FortiGate will be configured with an [automation stitch](https://docs.fortinet.com/document/fortigate/7.6.4/administration-guide/139441/automation-stitches) which responds to a security event by invoking a Google Cloud Run Function, which will use data provided by FortiGate to find a compromised host VM and quarantine it.


### Learning Objectives

- Learn how to deploy Active/Passive FortiGate architecture in GCP using Terraform.
- Learn to create external threat feeds in FortiGate.
- Learn how FortiGate interoperates with GCP Cloud Function to automate incident response.
 

{{< figure src="base-env.png" alt="base-env" >}}
