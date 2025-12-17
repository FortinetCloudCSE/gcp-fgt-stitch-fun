---
title: "Ch 4 - Configure GCP Firewall and Test"
chapter: false
linkTitle: "Ch 4: Configure GCP and Test"
weight: 40
---

### **Configure Firewall rule and Test**

We are going to be configuring a firewall rule in the GCP trust VPC, which blocks all traffic from a source device with a Network Tag of "compromised".  When the Cloud Run Function recieved the notification and log from FortiGate, it will use the source ip address from that log to determine the device ID of the compromised host. It will then assign the Network tag to that host, effectively quarantining it.
