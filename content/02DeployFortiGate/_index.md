---
title: "Deploy FortiGates"
linkTitle: "Deploy FortiGates"
weight: 20
---

### ***Clone Github Repository and Deploy FortiGates using Terraform. 20min***

Qwiklabs has the ability to pre-deploy a fully functional environment with all of the underlying resources needed.  Where is the fun in that?  As this is an automation lab, we thought students would appreciate a little practice deploying infrastructure using Terraform.

The next few chapters will walk you through this process.  The result will be a security services Hub with two FortiGates in A/P configuration, along with a Debian 12 linux VM which we will use for the testing.  The FortiGates are deployed as backend sets to two pass through load-balancers.  While high availability is not needed for this lab, this is a very common deployment and students will potentially benefit from seeing this used in practice.

{{< figure src="no-fun.png" alt="no-fun" >}}
