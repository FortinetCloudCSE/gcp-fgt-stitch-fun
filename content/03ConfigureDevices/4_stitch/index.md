---
title: "Task 4 - Configure FortiGate Automation Stitch"
linkTitle: "Automation Stitch"
chapter: false
weight: 52
---

|                            |    |  
|----------------------------| ----|
| **Goal**                   | Enable automation stitch
| **Task**                   | Log into FortiGate GUI and configure stitch components|
| **Verify task completion** | Automation stitch is present|

### Automation Stitch

Now that we have our policy configured and set to log violations, we are going to configure an automation stitch in FortiGate.  The automation stitch consists of three components:

- Trigger - This is what starts the stitch
- Action - This is what the FortiGate will do when triggered
- Stitch - This is what ties Triggers and Actions together

For more documentation about about FortiGate Automation stitches, check out this [link](https://docs.fortinet.com/document/fortigate/7.6.4/administration-guide/139441/automation-stitches).

1. **View Trigger**

* Using the left navigation pane on FortiGate, navigate to **Security Fabric** > **Automation** > **Trigger**

* There are several default triggers available on FortiGate.  For this exercise, we will use one called **Traffic Violation**.  If you scroll down, you should see it in the list, along with a description of what it does.

2. **Create Action**

* Click on the **Action** tab.

* Select **Create new** at the top of the screen

* Scroll down to the **Cloud Compute** section and select **Google Cloud Function**

* Configure the Action as below:

  {{< figure src="new-act.png" alt="new-act" >}}

{{% notice tip %}} You can find the correct url for your cloud run function from cloud shell.  At the prompt, type ``` cd gcp-fgt-stitch-fun/terraform/gcp-cloud-run-log-request/ ``` and then type ``` terraform output ```. {{% /notice %}}

3. **Create Stitch**

* Click on the **Stitch** tab

* Select **Create new** at the top of the screen

* Configure the stitch as below and click **OK**:

  {{< figure src="new-stitch.png" alt="new-stitch" >}}

{{< quizframe page="/gamebytag?tag=config" height="800" width="100%" >}}

### This chapter is complete! Congratulations. You can move to the next Chapter
