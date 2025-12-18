---
title: "Task 3 - Configure FortiGate Policy"
linkTitle: "FortiGate Policy"
chapter: false
weight: 50
---

|                            |    |  
|----------------------------| ----|
| **Goal**                   | Enable threat feed in FortiGate Policy|
| **Task**                   | Create new Policy in FortiGate which uses threat feed as destination IP|
| **Verify task completion** | Policy is present|

### FortiGate Policy

Now that we have our external threat feed, let's configure a policy which blocks packets with a destination IP matching that list.  

1. **Create Policy**
        
* Using the left navigation pane on FortiGate, navigate to **Policy & Objects** > **Firewall Policy**

* Click on **Create new**

* Configure the policy as below:
  - For Destination, click the "+" and in the dropdown, select **Imported & Dynamic Address**.  Your threat feed should be there.  Select it.
  {{< figure src="new-pol.png" alt="new-pol" >}}

* The new policy will show up in the list as the second policy.  This presents a problem, because traffic is matched to a policy in the order in which they are configured.  Once a policy is matched, there is no further processing.  This means that the traffic we want to stop would be allowed by our outbound policy before it is measured by our block-threats policy.

  {{< figure src="pol-ord1.png" alt="pol-ord1" >}}

* In order to fix this issue and have this function as expected, we will need to rearrange the policies.  This is done by clicking on the policy you want to move and "dragging" it into the correct postion.  When done it should look someting like below

  {{< figure src="pol-ord2.png" alt="pol-ord2" >}}

### Move to the next task
