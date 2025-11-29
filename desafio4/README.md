# Desafio 4 — Microsserviços Independentes

## Objetivo

Implementar dois microsserviços independentes que se comunicam via HTTP:
- **User Service**: Fornece dados de usuários (porta 5001)
- **Activity Service**: Fornece atividades e consome User Service (porta 5002)

## Componentes

| Componente | Descrição |
|-----------|-----------|
| **service-users** | Flask - Gerencia usuários :5001 |
| **service-activities** | Flask - Gerencia atividades :5002 |
| **microservices-network** | Rede Docker para comunicação |

## Quick Start

### 1. Executar
```bash
cd desafio4
./run.sh
```

### 2. Testar endpoints

**User Service:**
```bash
curl http://localhost:5001/users           # Lista usuários
curl http://localhost:5001/users/1         # Usuário específico
curl http://localhost:5001/health          # Health check
```

**Activity Service:**
```bash
curl http://localhost:5002/activities      # Lista atividades
curl http://localhost:5002/activities/1    # Atividades do usuário 1
curl http://localhost:5002/users-with-activities  # Dados combinados
```

### 3. Visualizar logs
```bash
docker logs -f service-users
docker logs -f service-activities
```

### 4. Parar
```bash
./stop.sh
```

## Teste de Resiliência

```bash
# Parar User Service
docker stop service-users

# Activity Service retorna erro apropriado
curl http://localhost:5002/users-with-activities

# Reiniciar
docker start service-users
```

## Conceitos-chave

✅ Arquitetura de microsserviços  
✅ Comunicação HTTP entre serviços  
✅ Isolamento de responsabilidades  
✅ Independência de deploy  
✅ Resiliência em falhas  
✅ Agregação de dados de múltiplos serviços
