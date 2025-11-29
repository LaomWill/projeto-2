#!/bin/bash

echo "=========================================="
echo "Parando e removendo containers..."
echo "=========================================="
echo ""

docker stop web-server http-client 2>/dev/null
docker rm web-server http-client 2>/dev/null
docker network rm desafio1-network 2>/dev/null

echo "Containers e rede removidos com sucesso!"
echo ""
