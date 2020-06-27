FROM python:3.8-alpine
EXPOSE 5000

COPY requirements.txt /abagdemo/requirements.txt
WORKDIR /abagdemo
RUN pip3 install -r requirements.txt

COPY . /abagdemo
# Get the version of image from the k8s deployment and create
# a file named version.txt with the application version.
# Then delete the k8s deploy file because we don't need it any more.
RUN sed -r -n 's/appVersion:\s+(.*)/\1/p' helm/abagdemo/Chart.yaml | sed -e 's/^[ \t]*//' > version.txt && rm helm/abagdemo/Chart.yaml && rmdir helm/abagdemo -p --ignore-fail-on-non-empty
# ENTRYPOINT ["/abagdemo/runit.sh"]