**Introduction**
This repo houses the abagdemo app and provides an example of how to build it using Google Cloud Builder.

**Credentials**
The cloudbuild.yaml script requires that the Google Storage credentials that abagdemo needs are stored using Secret Manager.
The name of the secret is 'last-baron-abagdemo', or whatever you set "_GS_CREDS" equal to at the bottom of cloudbuild.yaml.
It must contain the Key .json file of the creds that can get to Google Storage.

Also, GitHub credentials are required so that the pipeline can add a Tag to the Git repo at merge time.  
These are also stored in Secret Manager as "fkuligowski-git-user" and "fkuligowski-git-pwd", or whatever you set "_GIT_USER" and "_GIT_PWD" equal to at the bottom of cloudbuild.yaml.  

**Install**

I had trouble with "pip3 install -r requirements.txt" with the google-cloud-storage library. It would get an error saying *error: invalid command 'bdist_wheel*. To fix this, [this post](https://stackoverflow.com/questions/34819221/why-is-python-setup-py-saying-invalid-command-bdist-wheel-on-travis-ci) said to "pip3 install wheel", which fixes the issue, so I added wheel to the requirements.txt. But I still got that error when it was right before google-cloud-storage. I had to move wheel to the top of the file, then the error stopped coming up. (I'm not sure this isn't going to come back later, though).

**Docker**

Create the image for abagdemo

```
docker build -t fckuligowski/abagdemo:v1.x .
```

If you want to run the container from Docker, and shell into it.
```
docker run --rm -td fckuligowski/abagdemo:v1.x 
docker ps
docker exec -it f1048684b081 /bin/sh
docker stop f1048684b081
```

This was the old way I was running it.

```
docker run --name abagdemo -d -p 30080:5000 --rm -v instance/creds/justademo-acoustic-apex.json=/abagdemo/justademo-acoustic-apex.json -e GOOGLE_APPLICATION_CREDENTIALS=/abagdemo/instance/creds/justademo-acoustic-apex.json fckuligowski/abagdemo:v1.1
or
docker run --name abagdemo -p 30080:5000 --rm -v instance/creds/justademo-acoustic-apex.json=/abagdemo/justademo-acoustic-apex.json -e GOOGLE_APPLICATION_CREDENTIALS=/abagdemo/instance/creds/justademo-acoustic-apex.json fckuligowski/abagdemo:v1.1
```
If you want to run pytest to test it from Docker
```
docker run --name abagdemo -p 30080:5000 --rm -e MODE='TESTING' -v instance/creds/justademo-acoustic-apex.json=/abagdemo/justademo-acoustic-apex.json -e GOOGLE_APPLICATION_CREDENTIALS=/abagdemo/instance/creds/justademo-acoustic-apex.json -v ~/py/abagdemo/tests/:/abagdemo/tests fckuligowski/abagdemo:v1.1
```
Note that the image name needs to be at the end of the command, after the "-e" env var parms (else Docker will pass them to the shell script as arguments, not env vars).

Docker push to repo

```
docker push fckuligowski/abagdemo:v1.0
```

