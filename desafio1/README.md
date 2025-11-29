# Desafio 1 — Containers em Rede

## Objetivo

Implementar a comunicação entre dois containers Docker em uma rede customizada:
- **Servidor**: Flask rodando na porta 8080
- **Cliente**: Script que faz requisições HTTP a cada 5 segundos

## Componentes

| Componente | Descrição |
|-----------|-----------|
| **web-server** | Servidor Flask (Python 3.11) na porta 8080 |
| **http-client** | Cliente que faz requisições periódicas |
| **desafio1-network** | Rede Docker customizada para comunicação |

## Quick Start

### 1. Iniciar
```bash
cd desafio1
./run.sh
```

### 2. Visualizar logs
```bash
docker logs -f web-server    # Logs do servidor
docker logs -f http-client   # Logs do cliente
```

### 3. Parar
```bash
./stop.sh
```

## Endpoints do Servidor

- `GET /` - Retorna JSON com hostname, timestamp e contador de requisições
- `GET /health` - Health check

## Testar Manualmente

```bash
curl http://localhost:8080
```

## Limpeza Completa

```bash
docker stop web-server http-client
docker rm web-server http-client
docker network rm desafio1-network
```

## Conceitos-chave

✅ Redes Docker customizadas  
✅ Comunicação entre containers por nome  
✅ Isolamento de rede  
✅ DNS interno do Docker
