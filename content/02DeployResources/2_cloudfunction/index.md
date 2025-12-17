---
title: "Task 2 - Deploy Cloud Function and Firestore"
linkTitle: "Deploy Function"
weight: 20
---

In this task we will create the Google Cloud Run Function, which handles device quarantine.  In order to track mitigations, and to prevent repeditive processing we are also creating a Firestore database.  Prior to starting that we need to create the default Firestore database and enable the Cloud Run Admin API.

### Enable services

1. **Create Default Firestore Database**

* From the Search bar at the top of the Google Cloud Console, type ``` Firestore ``` and click on the first option.

 {{< figure src="find-fs.png" alt="find-fs" >}}

* Click on **Create a Firestore database**

 {{< figure src="create-fs.png" alt="create-fs" >}}

* Now we are going to create our "(default)" database.  You will leave **ALL** default values in place and click on **Create Database** at the bottom of the page

 {{< figure src="fs-def.png" alt="fs-def" >}}

* If your creation was successful, you should see a screen like below:

 {{< figure src="def-yes.png" alt="def-yes" >}}

1. **Enable Cloud Run Admin API**

* From the "hamburger" menu in the Google Cloud Console, navigate toe **APIs & Services**

* Click on **Enable APIs and services**

 {{< figure src="en-api.png" alt="en-api" >}}

* In the search bar, type ``` cloud run admin api ``` and then select the result

 {{< figure src="cra-api.png" alt="cra-api" >}}

* On the next screen select **Enable**

### Deploy Cloud Run Function and Database using Terraform

1. Deploy resources
  
* From the Cloud Shell, Navigate to the Cloud Run Function  deployment directory by typing ``` cd gcp-fgt-stitch-fun/terraform/gcp-cloud-run-log-request ```

* At the prompt, issue the ``` terraform init ``` command.  You should get a message stating **Terraform has been successfully initialized!**

* For this next step, you will need to input your GCP project ID.  As before, you can ou can either use ``` ctrl + c ``` or ``` cmd + c ``` to copy the Project ID.

* Now issue the ``` terraform apply --auto-approve ``` command.

* You will be prompted to "Enter a value:" for **var.project_id**.  Use ``` ctrl + v ``` or ``` cmd + v ``` and then it enter.

* The deployment will take some time to complete.  Take note of the outputs scrolling on the screen.

* There will be a number of outputs at the bottom of the screen.  For example:

```sh

Apply complete! Resources: 4 added, 0 changed, 0 destroyed.

Outputs:

curl_test_command = <<EOT
# Test with GET request
curl "https://my-request-logger-7cyclxf27q-uc.a.run.app?test=true&user=demo"
    
# Test with POST request and JSON data
curl -X POST "https://my-request-logger-7cyclxf27q-uc.a.run.app" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token" \
  -H "X-Custom-Header: demo-value" \
  -d '{"message": "Hello from test", "timestamp": "2025-12-10", "data": {"key": "value"}}'

EOT
function_name = "my-request-logger"
function_project = "qwiklabs-gcp-02-da0cd80e4e00"
function_region = "us-central1"
function_url = "https://my-request-logger-7cyclxf27q-uc.a.run.app"
logs_command = "gcloud functions logs read my-request-logger --region=us-central1 --limit=50"
source_bucket_name = "my-request-logger-source-21997644"
student_04_e6938c5f38ce@cloudshell:~/gcp-fgt-stitch-fun/terraform/gcp-cloud-run-log-request (qwiklabs-gcp-02-da0cd80e4e00)$

```

### Test Function

* SSH to Debian VM

* Copy the curl command from the Terraform outputs in **your environment** (do not use the examples from this document) and paste them into the CLI of your Debian VM.  You should se something like

```sh

student-04-e6938c5f38ce@a-debian-vm-mkq:~$ curl -X POST "https://my-request-logger-7cyclxf27q-uc.a.run.app" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token" \
  -H "X-Custom-Header: demo-value" \
  -d '{"message": "Hello from test", "timestamp": "2025-12-10", "data": {"key": "value"}}'

{
  "status": "success",
  "message": "Request logged successfully",
  "logged_at": "check Cloud Logging for details",
  "request_summary": {
    "method": "POST",
    "path": "/",
    "headers_count": 13,
    "query_params_count": 0,
    "has_body": true
  },
  "traffic_violation": null
}
student-04-e6938c5f38ce@a-debian-vm-mkq:~$

```

* From the Google Cloud Console search bar, typ ``` cloud run functions ``` and choose the first option

* On the left menu, select **Services**

* You should see a service named **my-request-logger**.  Click on that to see the Service details

* Now select **Logs**.  In the logs, you should see a few messages indicating that the cloud function was called

 {{< figure src="cf-logs.png" alt="cf-logs" >}}

