import pytest
from unittest import TestCase
import subprocess
import os
import sqlalchemy as sa
from time import sleep


class BasicUnitTest(TestCase):
    pass


class BasicIntegrationTest(TestCase):
    pass


@pytest.mark.usefixtures("docker_compose_db_migrate")
class DBIntegrationTest(TestCase):
    db_uri = os.environ.get("DATABASE_URI", "postgresql+psycopg2://mat_admin:passwd@localhost/mat")
    engine = sa.create_engine(db_uri)


@pytest.yield_fixture(scope="class")
def docker_compose_db_migrate():
    # Create new docker volume for testing; remove it if it currently exists
    test_volume_name = "postgresql-data-mat-test"
    result = subprocess.run(
        ["docker", "volume", "rm", "-f", test_volume_name], capture_output=True, text=True
    )
    assert result.returncode == 0
    result = subprocess.run(
        ["docker", "volume", "create", test_volume_name], capture_output=True, text=True
    )
    assert result.returncode == 0
    # Override volume name environment variable for db container
    os.environ["POSTGRES_DATA_VOLUME_NAME"] = test_volume_name
    # Use subprocess module to call docker compose up in detached state
    result = subprocess.run(
        ["docker-compose", "up", "-d", "db-migrate"], capture_output=True, text=True
    )
    assert result.returncode == 0
    # Sleep long enough to allow migration to complete
    sleep(60)  # TODO look into changing to an assert that the migration container exited successfully
    yield

    # TODO: Capture docker compose logs to file
    # Call docker compose down for clean up
    result = subprocess.run(
        ["docker-compose", "down"], capture_output=True, text=True
    )
    assert result.returncode == 0
    # Remove docker volume used for testing
    result = subprocess.run(
        ["docker", "volume", "rm", "-f", test_volume_name], capture_output=True, text=True
    )
    assert result.returncode == 0
    # NOTE: try to capture general pattern, repeat for other egress options e.g. Kafka or Blob
