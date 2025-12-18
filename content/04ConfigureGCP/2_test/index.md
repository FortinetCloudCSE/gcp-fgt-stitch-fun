---
title: "Task 2 - Let's Test It"
linkTitle: "Test Function"
chapter: false
weight: 5
---

|                            |    |  
|----------------------------| ----|
| **Goal**                   | Confirm service is working|
| **Task**                   | Verify blocked traffic, verify quarantine|
| **Verify task completion** | Traffic is blocked and device is quarantined|


### Test time

1. **Debian**

* SSH to your Debian VM by navigating to **Compute Engine** > **VM instances**

* At the prompt, type ``` ping 8.8.8.8 ``` and hit enter

* This ping should fail.

2. **FortiGate**

* Log into the primary FortiGate.  Username ``` admin ``` Password ``` D3v0ps@1234! ```

* Navigate to **Log & Report** > ***Forward Traffic***

* You should see the denied pings.

  {{< figure src="denied.png" alt="denied" >}}

* Navigate to **Log & Report** > ***System Events***

* You should see the **Automation stitch triggered** event.  Click on it.

* You will see that the custom-stitch was triggered

3. **Debian**

* In the Google Cloud Console, Navigate to **Compute Engine** > **VM instances** and select the Debian VM to see details

* Scroll down to **Network tags** and note that the **compromised** tag is set.

  {{< figure src="net-tags.png" alt="net-tags" >}}

* SSH to your Debian VM by navigating to **Compute Engine** > **VM instances**

* Type ``` curl www.fortinet.com ``` at the prompt.  This should fail because the VM is quarantined.

4. **Cloud Function Logs**

* Navigate to **Cloud Run Functions** > **Services** > **my-request-logger**

* Click on **Logs**.  Scroll through them.  You should see some logs like below:

  {{< figure src="sample-logs.png" alt="sample-logs" >}}

5. **Firestore**

* Navigate to **Firestore and select the **(default)** database we creted earlier

* Click on **processed_source_ips**

* You should see the source IP for the Debian VM

  {{< figure src="db-check.png" alt="db-check" >}}

{{< quizframe page="/gamebytag?tag=test" height="800" width="100%" >}}

### Congratulations!  You have completed this Class!
