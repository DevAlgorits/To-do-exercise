# Task Management API

Este projeto é uma API de gerenciamento de tarefas construída com **FastAPI**, oferecendo endpoints para autenticação, gerenciamento de tarefas e cache com Redis. O sistema utiliza MongoDB para persistência de dados.

## Funcionalidades

- **Gerenciamento de Tarefas**
  - Adicionar uma nova tarefa.
  - Listar todas as tarefas.
  - Atualizar tarefas existentes.
  - Excluir tarefas.
- **Autenticação**
  - Login com geração de tokens JWT.
  - Verificação de token para endpoints protegidos.
  - Logout com revogação de tokens.
- **Cache**
  - Integração com Redis para armazenamento temporário de tarefas.

## Pré-requisitos

- Python 3.10 ou superior
- MongoDB configurado e rodando
- Redis configurado e rodando

