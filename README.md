# Gerador de Boletos

- Após clonar o repositório e navegar até sua raiz com um terminal:
    - Crie o arquivo /dotenv_files/.env com ```cp dotenv_files/.env-sample .env```
    - Substitua os valores com "change-me" em .env
    - Para a variável SECRET_KEY, será necessário gerar uma nova chave com o comando abaixo:
        - ```python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" ```
        - Copie a chave e cole entre aspas em SECRET_KEY=

- Agora, basta rodar um ```make up``` e aguardar o projeto subir.
    - Caso tenha problemas com conflitos de outros containeres aqui, rode:
        - ```make down FORCE=true``` e, depois,
        - ```make up```
    - ```make help``` irá mostrar todos os comandos disponíveis

- Com o projeto rodando (deverão estar rodando 4 containeres: *web*, *db*, *redis* e *celery*), realize a importação de um arquivo .csv no endpoint http://localhost:8000/upload-csv/
    - No terminal, por exemplo: ```curl -X POST http://localhost:8000/upload-csv/ -F "file=@path/to/you/file.csv"```
        - Substitua ```path/to/you/file.csv``` pelo caminho para seu arquivo
    - Na raiz do projeto há um arquivo *input_short.csv* com apenas 100.000 linhas, para testes breves:
        Com o terminal na raiz do projeto: ```curl -X POST http://localhost:8000/upload-csv/ -F "file=@input_short.csv"```