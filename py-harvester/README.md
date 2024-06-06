# py-harvester

POC python program to harvest market data (AlphaVantage API data) and push records to a Kafka topic.

## Overview
Poetry is used to manage dependencies and packaging. The program is packaged as a Docker image and can be run as a container.

The docker image can be built locally within this project directory using the Dockerfile provided in the `docker` directory:

```bash
docker build --tag <image-name> --file docker/App.dockerfile .
```

Alternatively, the container can be built as part of the `docker compose build` process.

## Poetry usage

Install poetry:
```bash
pip install poetry
```

Install dependencies:
```bash
poetry install
```

Run the program:
```bash
poetry run python -m py_harvester
```

Run the tests:
```bash
poetry run coverage run --rcfile ./pyproject.toml -m pytest tests
```



