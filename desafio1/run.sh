#!/bin/bash

echo "=========================================="
echo "Desafio 1 - Containers em Rede"
echo "=========================================="
echo ""

# Criar rede customizada
echo "1. Criando rede Docker customizada 'desafio1-network'..."
docker network create desafio1-network
echo ""

# Build das imagens
echo "2. Construindo imagem do servidor..."
docker build -t desafio1-server -f Dockerfile.server .
echo ""

echo "3. Construindo imagem do cliente..."
docker build -t desafio1-client -f Dockerfile.client .
echo ""

# Executar containers
echo "4. Iniciando container do servidor (web-server)..."
docker run -d --name web-server --network desafio1-network -p 8080:8080 desafio1-server
echo ""

echo "5. Aguardando servidor inicializar..."
sleep 3
echo ""

echo "6. Iniciando container do cliente (http-client)..."
docker run -d --name http-client --network desafio1-network desafio1-client
echo ""

echo "=========================================="
echo "Containers iniciados com sucesso!"
echo "=========================================="
echo ""
echo "Para visualizar os logs:"
echo "  - Servidor: docker logs -f web-server"
echo "  - Cliente:  docker logs -f http-client"
echo ""
echo "Para acessar o servidor localmente:"
echo "  - http://localhost:8080"
echo ""
echo "Para parar os containers:"
echo "  ./stop.sh"
echo ""
