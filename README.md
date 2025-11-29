# Projeto 2 - Fundamentos de Computação Concorrente, Paralela e Distribuída

**Disciplina:** Fundamentos de Computação Concorrente, Paralela e Distribuída  
**Professor:** Jorge Soares de Farias Júnior  
**Aluno:** Luan Martins de Souza  
**Turma:** ASD20252_4A  

---

## 📦 Coleção de Desafios de Microsserviços e Arquitetura

Uma série de desafios práticos que exploram conceitos essenciais de microsserviços, containerização com Docker e orquestração com Docker Compose.

## 🎯 Objetivos dos Desafios

| Desafio | Objetivo | Aplicação Prática |
| :---: | :--- | :--- |
| **1** | Comunicação Cliente-Servidor | Serviço e cliente conteinerizados separadamente com rede Docker |
| **2** | Orquestração Simples | Ambiente multi-container com Docker Compose |
| **3** | Aplicação Conteinerizada | Aplicação Python pronta para Docker com gerenciamento de dependências |
| **4** | Interação entre Serviços | Dois microsserviços comunicando-se via HTTP/REST |
| **5** | Arquitetura Completa | Sistema completo de e-commerce com API Gateway e serviços de domínio |

---

## 🏗️ Detalhamento de Cada Desafio

### **Desafio 1: Comunicação Cliente-Servidor**
Sistema básico de comunicação entre dois componentes isolados.

- **Arquivos principais:** `server.py`, `client.py`, `Dockerfile.server`, `Dockerfile.client`
- **Aprendizado:** Conteinerização, redes Docker customizadas, comunicação intra-container

### **Desafio 2: Orquestração Simples**
Configuração boilerplate para ambiente multi-container.

- **Arquivos principais:** `docker-compose.yml`, scripts de automação
- **Aprendizado:** Docker Compose, definição declarativa de serviços

### **Desafio 3: Aplicação Conteinerizada**
Preparação de aplicação Python para ambiente Docker.

- **Arquivos principais:** `app.py`, `requirements.txt`, `Dockerfile`, `docker-compose.yml`
- **Aprendizado:** Gerenciamento de dependências, otimização de imagens, orquestração

### **Desafio 4: Interação entre Serviços**
Demonstração de comunicação entre microsserviços independentes.

- **Arquivos principais:** `service_a/`, `service_b/`, configuração de rede
- **Aprendizado:** Descoberta de serviços, APIs REST, comunicação síncrona

### **Desafio 5: Arquitetura de Microsserviços Completa**
Sistema complexo típico de aplicações reais.

- **Arquivos principais:** `gateway/`, `ms_users/`, `ms_orders/`, `docker-compose.yml`
- **Aprendizado:** Padrão API Gateway, DDD (Domain-Driven Design), orquestração avançada

---

## 🚀 Como Iniciar

### Pré-requisitos
```bash
docker --version      # v20.10+
docker-compose --version  # v2.0+
```

### Executar um Desafio
```bash
# 1. Entrar no diretório
cd desafioX  # Substituir X por 1-5

# 2. Construir e iniciar
docker-compose up --build -d

# 3. Verificar execução
docker-compose ps

# 4. Encerrar
docker-compose down
```

### Verificar Logs
```bash
docker-compose logs -f
```

---

## 📂 Organização do Repositório

Cinco desafios independentes, cada um em seu próprio diretório:
- `desafio1/` → Redes e comunicação
- `desafio2/` → Orquestração básica
- `desafio3/` → Containerização completa
- `desafio4/` → Microsserviços
- `desafio5/` → Arquitetura avançada

---

## 🎓 Conceitos Cobertos

**Docker:** Containers, Imagens, Dockerfiles, Networking  
**Orquestração:** Docker Compose, dependências, saúde de serviços  
**Microsserviços:** Isolamento, APIs REST, resiliência, gateway  
**Persistência:** Volumes, bancos de dados  

---

## 📝 Instruções Genéricas

1. **Navegação:** Entre no diretório `desafioX` desejado
2. **Inicialização:** Execute `docker-compose up --build -d`
3. **Monitoramento:** Use `docker-compose ps` para verificar status
4. **Encerramento:** Finalize com `docker-compose down`

Cada desafio possui um `README.md` individual com instruções específicas.

