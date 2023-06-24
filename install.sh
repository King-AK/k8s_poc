POSTGRES_RELEASE_NAME=$1
KAFKA_RELEASE_NAME=$2
POSTGRESSQL_VERSION=12.5.8
KAFKA_VERSION=22.1.6

# Add repo if not already present
helm repo add bitnami https://charts.bitnami.com/bitnami

# Install Bitnami PostgreSQL
helm install -f .helm-config/postgres-values.yml $POSTGRES_RELEASE_NAME bitnami/postgresql --version $POSTGRESSQL_VERSION

# Install Bitnami Kafka
helm install -f .helm-config/kafka-values.yml $KAFKA_RELEASE_NAME bitnami/kafka --version $KAFKA_VERSION

# Apply K8s files
k apply -f .k8s-configs/
k apply -f .k8s/