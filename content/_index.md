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

This lab will explain how to use the FortiGate automation stitch integration with GCP cloud functions in order to automatically respond to security events. For our scenario, we will configure an Active/Passive High Availability pair of FortiGate VMs in a Security Services Hub. The FortiGate security policy will block the threatening traffic but will be configured with an automation stitch, which further responds to a security event by invoking a Google Cloud Run Function.  This Function contains a Python script which will identify the offending device, using the source IP from the information sent by FortiGate.  Once identified, the device will be quarantined.

### Learning Objectives

- Learn how to deploy Active/Passive FortiGate architecture in GCP using Terraform.
- Learn to create external threat feeds in FortiGate.
- Learn how FortiGate interoperates with GCP Cloud Function to automate incident response.
 

{{< figure src="base-env.png" alt="base-env" >}}

### FortiGate Automation Stitch

FortiGate Automation Stitches are powerful orchestration tools that enable automated responses to security events in real-time. An automation stitch consists of two main components: a **trigger** (such as a security event, log entry, or system condition) and one or more **actions** (like sending notifications, executing scripts, or calling external APIs). When a trigger condition is met, the FortiGate automatically executes the predefined actions without requiring human intervention. This creates a seamless, event-driven security response system that can react to threats in milliseconds rather than minutes or hours.

The benefits of using FortiGate Automation Stitches are substantial for modern cybersecurity operations. They dramatically reduce **Mean Time to Response (MTTR)** by eliminating the delay between threat detection and remediation actions. Organizations can achieve **consistent, repeatable responses** to security incidents, removing the variability of manual processes and ensuring that critical security procedures are always followed. Automation stitches also enable **scalable security operations**, allowing a single FortiGate to manage thousands of automated responses simultaneously without overwhelming security teams. Additionally, they provide **enhanced integration capabilities** with cloud platforms, SIEM systems, and other security tools, creating a unified security ecosystem that can coordinate complex, multi-step incident response workflows across hybrid and multi-cloud environments.

More information can be found in the FortiGate automation stitch [documentation](https://docs.fortinet.com/document/fortigate/7.6.4/administration-guide/139441/automation-stitches).

### FortiGate External Threat Feed

FortiGate External Threat Feeds are dynamic security intelligence sources that automatically import and update threat indicators from external databases, security vendors, and threat intelligence platforms. These feeds provide real-time access to malicious IP addresses, domains, URLs, and file hashes that have been identified by global security communities and commercial threat intelligence providers. FortiGate can consume feeds in various formats including structured threat intelligence formats (STIX/TAXII), simple text files, and API-based feeds. Once configured, the FortiGate automatically downloads updated threat indicators at regular intervals, ensuring that security policies remain current with the latest threat landscape without manual intervention.

The benefits of using External Threat Feeds significantly enhance an organization's security posture and operational efficiency. They provide **proactive threat prevention** by blocking known malicious entities before they can establish connections or deliver payloads to internal networks. **Automated threat intelligence updates** eliminate the manual effort required to maintain current blacklists and ensure that security teams always have access to the latest threat indicators from multiple sources. External threat feeds also enable **contextual security decisions**, allowing FortiGate to make informed blocking or monitoring decisions based on threat severity, source credibility, and organizational risk tolerance. Additionally, they support **compliance and forensics requirements** by providing detailed logging and attribution data that helps security teams understand threat patterns and demonstrate due diligence in threat mitigation efforts.

### Google Cloud Run Function

Google Cloud Run Functions are serverless, event-driven compute services that automatically execute code in response to HTTP requests, cloud events, or direct invocations. Built on Google's highly scalable infrastructure, Cloud Run Functions allow developers to deploy containerized applications without managing servers, operating systems, or runtime environments. These functions can be written in multiple programming languages including Python, Node.js, Go, and Java, and they automatically scale from zero to thousands of instances based on incoming request volume. The serverless nature means you only pay for the compute time actually used during function execution, making it extremely cost-effective for sporadic or unpredictable workloads.

The benefits of using Google Cloud Run Functions for security automation are compelling for modern cloud architectures. They provide **instant scalability** to handle security events ranging from single incidents to massive attack waves without pre-provisioning resources. The **event-driven architecture** integrates seamlessly with other GCP services like Pub/Sub, Cloud Storage, and monitoring systems, enabling sophisticated incident response workflows. **Zero infrastructure management** eliminates the operational overhead of maintaining servers, allowing security teams to focus on developing effective response logic rather than infrastructure maintenance. Additionally, Cloud Run Functions offer **built-in security features** including automatic TLS termination, IAM-based access control, and VPC connectivity, ensuring that automated security responses are themselves secure and compliant with enterprise security requirements.


