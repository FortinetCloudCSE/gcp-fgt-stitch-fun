---
title: "Task 2 - Create External Threat Feed on FortiGate"
linkTitle: "Threat Feed"
chapter: false
weight: 5
---

|                            |    |  
|----------------------------| ----|
| **Goal**                   | Enable threat feed on FortiGate|
| **Task**                   | Log into FortiGate GUI and configure threat feed|
| **Verify task completion** | Blocked IP is present in threat feed|

### Threat feed

1. **Configure FortiGate**

* Log into FortiGate by typing https://\<fortigate ip>:8443 into your favorite browser window.

* Username is ``` admin ``` password is ``` D3v0ps@1234! ```

* Using the left side menu on the **Primary** FortiGate (most likely fgt1), navigate to **Security Fabric** > **External Connectors**

* Click on **Create New** at the top of the screen

* Scroll down to **External Feeds** and click on **IP Address**

  {{< figure src="add-feed.png" alt="add-feed" >}}

* Choose a **Name** for the threat feed.  This is arbitrary.

* Turn off **HTTP basic authentication** 

* Add ``` http://<debian-ip> ``` as ** URL of external resource.

* Verify that your feed configuration looks like below and then click **OK**

  {{< figure src="feed-conf.png" alt="feed-conf" >}}

* It may take a few seconds for the feed to come up.  It should eventually look like below.  Hover over the Icon and when the popup appears, click on **View Entries**

  {{< figure src="tf-green.png" alt="tf-green" >}}

* You should see that **8.8.8.8** is in the list and is **Valid**

### Move to the next task
