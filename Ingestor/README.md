# Harvester
* Connects to external sources, performs data schema enforcement, pushes data to a subsequent storage layer.
* Needs integration tests for both input and output.
* Unit test the schema enforcement in the middle.
* Current target output is a Postgres DB, but other output should include JSON files, Kafka Topics, etc. This way it can become more modular and even scale into the cloud in the future.
* JSON file output for example could go into temporary storage on the container and then be pushed into ADLS storage. Alternatively, the container could sit on top of cloud storage and write the JSON files directly into a "base area" to be handled by downstream services, e.g. a Databricks Cluster.

## Docker Container

* Container structure should copy the requirements file, be based on the Python3.7 (Alpine or Buster) image.
* Move towards making the container more than just a collection of scripts: it should be a living process that pulls stock and crypto data of interest on a timer, and then publishes schema enforced output data. Data which fails to meet schema enforcement processes should be logged as ERROR messages in a log system, but the container should not die or break.
* Command to build Harvester docker image (run from top level directory): `docker build -t harvester -f ./Docker/Harvester/Dockerfile .`

## Pull Integrations
## Push Integrations
### SQL Alchemy
* Use credentials passed to connect to a SQL Database, automatically migrate with the Alembic scripts, and then begin publishing data using the Flask models.
* When DB migration version < Harvester version, Harvester should try to upgrade the DB and wait if in the middle of migration. Upgrading the DB should also temporarily halt any other Harvester containers from pushing data.
* When DB migration version > Harvester version, Harvester should stop trying to push data to the DB and should wait for an update to the Image and a restart

# TODO
* Populate a requirements.txt file inside of the Harvester directory so that it will be copied into the image. 
* Container Registry with appropriate tagging when eventually signing up for a cloud service.
* rename "integration" folders to something more appropriate
* Make a cron job, or some kind of master python script that drives the container as a daemon and automatically pulls, enforces schema, and publishes.
* Then would need DockerFile/DockerCompose or whatever to understand that specific environment variables need to be set for interval data pulls, API key set up, publishing methods, etc.
* Figure out if can start containers as part of pytest conftest. If so, literally just plug in DB container versions for SQLAlchemy integration testing portions. 
* Also test migrations in addition to model data publishing.


# SQL stuff

Sample query to get put options where there is a chance to earn at least a 2% return by specified expiration date - FLESH THIS OUT, encapsulate in a function
```sql
SELECT * FROM options_time_series WHERE option_type='puts' AND symbol = 'T' AND strike*.02 <= bid AND expiration_date < '2021-10-18' AND strike <= (SELECT close FROM stock_time_series WHERE SYMBOL = 'T' AND datetime = (SELECT MAX(datetime) FROM stock_time_series WHERE SYMBOL='T'));
```