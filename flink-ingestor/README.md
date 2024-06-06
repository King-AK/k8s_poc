# flink-ingestor

POC scala program that works with stock market event data read from a Kafka topic. 
Very simply it reads the data, keys by symbol, calculates the running average volume, and writes this result to stdout.
When compiled, the program can be run as a Flink job.

## Overview
Gradle is used to manage dependencies and building. 
This program can be built as a Docker image and can be run as a container, supporting "Application Mode" style deployments for the Flink job.
The docker image can be built locally within this project directory using the Dockerfile provided in the `docker` directory:

```bash
docker build --tag <image-name> --file docker/App.dockerfile .
```

Alternatively, the container can be built as part of the `docker compose build` process.

## Gradle usage

Install gradle: 
    https://gradle.org/install/

Build the program:
```bash
gradle build
```

Run the tests:
```bash
gradle test
```



