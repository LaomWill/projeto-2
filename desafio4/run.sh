#!/bin/bash

echo "=========================================="
echo "Desafio 4 - Microsserviços Independentes"
echo "=========================================="
echo ""

# Criar rede
echo "1. Criando rede Docker 'microservices-network'..."
docker network create microservices-network
echo ""

# Build das imagens
echo "2. Construindo imagem do User Service..."
cd service-users
docker build -t user-service .
cd ..
echo ""

echo "3. Construindo imagem do Activity Service..."
cd service-activities
docker build -t activity-service .
cd ..
echo ""

# Executar containers
echo "4. Iniciando User Service (porta 5001)..."
docker run -d \
  --name service-users \
  --network microservices-network \
  -p 5001:5001 \
  user-service
echo ""

echo "5. Aguardando User Service inicializar..."
sleep 3
echo ""

echo "6. Iniciando Activity Service (porta 5002)..."
docker run -d \
  --name service-activities \
  --network microservices-network \
  -p 5002:5002 \
  -e USER_SERVICE_URL=http://service-users:5001 \
  activity-service
echo ""

echo "=========================================="
echo "Microsserviços iniciados com sucesso!"
echo "=========================================="
echo ""
echo "Endpoints disponíveis:"
echo ""
echo "User Service:"
echo "  - http://localhost:5001"
echo "  - http://localhost:5001/users"
echo "  - http://localhost:5001/users/active"
echo "  - http://localhost:5001/health"
echo ""
echo "Activity Service:"
echo "  - http://localhost:5002"
echo "  - http://localhost:5002/activities"
echo "  - http://localhost:5002/users-with-activities"
echo "  - http://localhost:5002/health"
echo ""
echo "Testar comunicação entre serviços:"
echo "  curl http://localhost:5002/users-with-activities"
echo ""
echo "Ver logs:"
echo "  docker logs -f service-users"
echo "  docker logs -f service-activities"
echo ""
echo "Parar serviços:"
echo "  ./stop.sh"
echo ""
