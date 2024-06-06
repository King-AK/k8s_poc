# k8s_poc

Dummy repo that uses K8s and Docker to play around with a microservices event architecture and do some polygot programming.

Market events are collected and curated from an API source.
They are then pushed into a Kafka topic.
Finally the events are consumed by an Apache Flink job.

## Overview

## Requirements

- docker
- [docker-compose](https://docs.docker.com/compose/install/#install-compose)
- kubernetes
- kubectl

## How to use

### docker compose

Build Images

```bash
docker compose build
```

Run services

```bash
docker compose up
```

Clean up and stop services

```bash
docker compose down
```

### Run with K8s

kompose convert

```bash
kompose -f docker-compose.yml convert -o k8s/
```

kubectl apply

```bash
kubectl apply k8s/
```

kubectl delete

```bash
kubectl delete k8s/
```
