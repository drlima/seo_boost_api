# SEO Boost API – Projeto de Curso

Este repositório contém o projeto base para o curso **SEO Boost API**, onde você aprenderá a criar uma API REST com FastAPI, integração com banco de dados PostgreSQL, autenticação, chamadas a modelos de IA generativa e muito mais.

## Instruções para rodar

1. Crie o ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute a aplicação:

   ```bash
   uvicorn app.main:app --reload

    ```

4. Acesse a documentação interativa:
   - Swagger UI: <http://localhost:8000/docs>
   - Redoc: <http://localhost:8000/redoc>

5. Para testar via terminal:

    ```bash
    http GET http://localhost:8000/
    ```

6. Para rodar os testes automatizados:

    ```bash
    pytest .
    ```
