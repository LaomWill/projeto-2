#!/bin/bash

echo "=========================================="
echo "Parando microsserviços..."
echo "=========================================="
echo ""

docker stop service-users service-activities 2>/dev/null
docker rm service-users service-activities 2>/dev/null
docker network rm microservices-network 2>/dev/null

echo "✓ Microsserviços parados e removidos!"
echo ""
