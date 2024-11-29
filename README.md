1. Linguagem e Frameworks
•	Linguagem: Python
•	Framework Backend: FastAPI
2. Banco de Dados
•	Banco Principal: MongoDB
o	Biblioteca de Conexão: ODMantic (para facilitar o trabalho com modelos e validação).
o	Motivo: Simplicidade no gerenciamento de dados no formato JSON-like e integração rápida com FastAPI.
•	Cache: Redis (para autenticação e otimização de acessos a dados).
o	Biblioteca: aioredis
o	Motivo: Requisito do case e utilidade prática para cache de sessões e autenticação JWT.
3. Autenticação e Autorização
•	Autenticação: JWT (JSON Web Tokens)
o	Biblioteca: PyJWT ou fastapi-jwt-auth.
o	Motivo: Seguro, fácil de usar e amplamente aceito no mercado.
•	Hash de Senhas: passlib (para gerar e verificar senhas).