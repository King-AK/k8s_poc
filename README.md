# k8s_poc

Dummy repo to play around with k8s and docker.

This is a lightweight repo with a microservices architecture that collects stock market data.

## Overview

## Requirements

- python3
- docker
- [docker-compose](https://docs.docker.com/compose/install/#install-compose)

## How to use

### Build Docker Images

```bash
docker compose build
```

### Run Container Structure Tests

```bash
container-structure-test test --image kingak/harvester-k8s-poc --config tests/container-structure-tests/harvester-file-existence-tests.yaml
container-structure-test test --image kingak/harvester-k8s-poc --config tests/container-structure-tests/harvester-metadata-test.yaml
container-structure-test test --image kingak/ingestor-k8s-poc --config tests/container-structure-tests/ingestor-file-existence-tests.yaml
container-structure-test test --image kingak/ingestor-k8s-poc --config tests/container-structure-tests/ingestor-metadata-test.yaml
```

### Run with Compose

```bash
docker compose up
```

### Run with K8s

```bash
kubectl apply -f .k8s/
```

## Development

### Running PyTest

### Running Container Structure Tests
