---
title: "Task 2 - Deploy Cloud Function and Firestore"
linkTitle: "Deploy Function"
weight: 20
---

In this task we will create the Google Cloud Run Function, which handles device quarantine.  In order to track mitigations, and to prevent repeditive processing we are also creating a Firestore database.  Prior to starting that we need to go and enable the Cloud Function and Firestore APIs

### Enable APIs

1. Enable Cloud Function API

* From the "hamburger" menu on the top left of the Googl Cloud Console, navigate to **APIs & Services**.

* Click on **Enable APIs and services

  {{< figure src="en-api.png" alt="en-api" >}}

* In the API Library search bar, typ ``` Cloud Function ``` and hit enter.

* Select Cloud Functions API

### Deploy Cloud Run Function and Database using Terraform

1. Deploy resources
  
* From the Cloud Shell, Navigate to the Cloud Run Function  deployment directory by typing ``` cd gcp-fgt-stitch-fun/terraform/gcp-cloud-run-log-request ```

* At the prompt, issue the ``` terraform init ``` command.  You should get a message stating **Terraform has been successfully initialized!**

* For this next step, you will need to input your GCP project ID.  As before, you can ou can either use ``` ctrl + c ``` or ``` cmd + c ``` to copy the Project ID.

* Now issue the ``` terraform apply --auto-approve ``` command.

* You will be prompted to "Enter a value:" for **var.project_id**.  Use ``` ctrl + v ``` or ``` cmd + v ``` and then it enter.

* The deployment will take some time to complete.  Take note of the outputs scrolling on the screen.

* There will be a number of outputs at the bottom of the screen.  For example: