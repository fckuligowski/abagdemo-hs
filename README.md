# abagdemo

This is a demo app for me (Frank Kuligowski) to try and do a DevOps pipeline.

The app is called **abagdemo**. It is meant to be an app that can record and show scan records for luggage bags, as they go through the airport conveyors. That's the premise for the app, so I had something to build for.

It is a Python Flask app that serves up a REST endpoint that one can use to interact with the app, at these endpoints (routes).

- /index is the home page
- /history/001 to show all the scans for bag id 001
- /status/001 to show just the latest scan for bag id 001
- /scan to add a new scan for a bag

The data is  stored in a Google Cloud Platform Storage object. It will automatically create the object on the fly, from a base data file in this repo. This requires GCP credentials. These can't be stored in the repo. They're stored in Google Secret Manager for testing, and in a Kubernetes Secret for 'production'.  The name of the Secret Manager object is "last-baron-abagdemo" and it contains the credential Key file.

This app uses pytest to do some tests, to ensure the app isn't broken.

The pipeline is written in Google Cloud Build script in a file named cloudbuild.yaml. It uses Cloud Builder to build a container, run the tests, and push the container to Google Container Registry. 

At Merge time, a tag is added to the GitHub repo, using the version found above. This requires GitHub creds so Cloud Build can write to the Git repo. These creds are also stored in Secret Manager as "fckuligowski-git-user" and "fckuligowski-git-pwd".

The name of the image that's pushed needs to be defined in "helm/abagdemo/values.yaml", except for the version tag which is stored in "helm/abagdemo/Chart.yaml". When that image tag value changes, Cloud Build will push the image to Container Registry (provided the tests  pass, and provided it is on a Merge).

The container image is deployed to 'production' with "helm install" at the end of the pipeline.

The container image doesn't do anything but install the app and it's Python requirements. Use the "runit.sh" script to start  the app in the container. Use the "tests/testit.sh" script to run the pytests from the container. Use the "rundev.sh" script to run the app from a container on your dev machine (I used a Linux Ubuntu host from Linux Academy).