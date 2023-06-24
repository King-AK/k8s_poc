POSTGRES_RELEASE_NAME=$1
KAFKA_RELEASE_NAME=$2

# Apply K8s files
kubectl delete -f .k8s/
kubectl delete -f .k8s-configs/

# Install Bitnami PostgreSQL
helm uninstall $POSTGRES_RELEASE_NAME

# Install Bitnami Kafka
helm uninstall $KAFKA_RELEASE_NAME
