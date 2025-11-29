#!/bin/bash

echo "=========================================="
echo "Limpando ambiente do Desafio 2..."
echo "=========================================="
echo ""

# Parar e remover containers
echo "1. Removendo containers..."
docker ps -a | grep -E "task-manager|data-reader" | awk '{print $1}' | xargs -r docker rm -f 2>/dev/null

# Remover imagens
echo "2. Removendo imagens..."
docker rmi task-manager data-reader 2>/dev/null

# Remover volume
echo "3. Removendo volume task-data..."
docker volume rm task-data 2>/dev/null

echo ""
echo "✓ Limpeza concluída!"
echo ""
