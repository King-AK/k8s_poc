# k8s_poc

Dummy repo to play around with k8s and docker.

This is a lightweight repo with a microservices architecture that collects market data from an API source, [AlphaVantage](https://www.alphavantage.co/), and publishes messages to a Kafka topic. A downstream subscriber consumes the messages and curates data before landing it into a relational database.

## Overview

## Requirements

- python3
- docker
- [docker-compose](https://docs.docker.com/compose/install/#install-compose)
- kubernetes
- kubectl
- helm

## How to use

### Build Docker Images

```bash
docker compose build
```

### Run with Compose

```bash
docker compose up
```

### Run with K8s

```bash
kubectl apply -f .k8s/
```

Not all services listed in the Compose file have to be translated to K8s services managed within this repo. Instead, selective use of Helm charts can help abstract certain pieces of the architecture such as PostgreSQL and Kafka. Then more focus can go to the custom code.

## Development

### Running Python Tests with PyTest

Set up and activate virtual environment

```bash
# Set up venv
rm -rf ./venv
python3.10 -m venv ./venv
source ./venv/bin/activate
```

Install requirements

```bash
# Install requirements
pip install --upgrade pip
pip install wheel
pip install setuptools
pip install -r requirements.txt
pip install -r test-requirements.txt
```

Lint Python Code

```bash
flake8
```

Run tests

```bash
pytest tests/
```

### Run Container Structure Tests

```bash
container-structure-test test --image kingak/harvester-k8s-poc --config tests/container-structure-tests/harvester-file-existence-tests.yaml
container-structure-test test --image kingak/harvester-k8s-poc --config tests/container-structure-tests/harvester-metadata-test.yaml
container-structure-test test --image kingak/ingestor-k8s-poc --config tests/container-structure-tests/ingestor-file-existence-tests.yaml
container-structure-test test --image kingak/ingestor-k8s-poc --config tests/container-structure-tests/ingestor-metadata-test.yaml
```
