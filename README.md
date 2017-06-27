# pyspark-hdfs-wordcount

This is a source-to-image application designed to be used on
[OpenShift](https://www.openshift.org) with the Apache Spark tooling of the
[radanalytics project](https://radanalytics.io).

## quick start

1. Install the [radanalytics bits](https://radanalytics.io/get-started)
1. run the following subsituting your HDFS host and port where appropriate:
   ```bash
   oc new-app --template=oshinko-pyspark-build-dc \
      -p APPLICATION_NAME=pyspark-hdfs-wordcount \
      -p GIT_URI=https://github.com/elmiko/pyspark-hdfs-wordcount
      -p APP_ARGS='--host=your.server.fqdn --port=someport'
   ```
1. expose a route to your application
   ```bash
   oc expose svc/pyspark-hdfs-wordcount
   ```
1. visit the route with a web browser, instructions be provided there
