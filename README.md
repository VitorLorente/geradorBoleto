# Gerador de Boletos

### Instruções de uso
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


### Sobre o projeto

- O projeto foi feito com tecnologias típicas da web: Django, Postgresql, Celery e Redis. Também foram utilizadas as bibliotecas:
    - django-postgres-copy -> Para performance ao salvar grande volume de dados no banco;
        - https://pypi.org/project/django-postgres-copy/
    - django_fsm -> Para controle rigoroso de transição de status dos boletos
        - https://docs.viewflow.io/fsm/index.html

- A ideia foi criar uma rotina de ETL que consegue realizar uma "pancada" grande no banco com boa performance, mas sem perder o rigor dos dados relacionais, e depois um fluxo de:
    - Verificação de consistência
    - Geração de boletos
    - Disparo de e-mails

- Os status controlados pela aplicação para cada boleto são:
    - *IMPORTED* - Assim que são importados
    - *CHECKS_PASSED* - Quando o boleto passa na verificação de consistência
    - *CHECKS_UNPASSED* - Quando o boleto não passa na verificação de consistência
    - *CHARGE_GENERATED* - Assim que é gerado a via do boleto
    - *EMAIL_SENT* - Quando os e-mails são gerados


- ATENÇÃO: Cada e-mail gera um log no console. Portanto, cuidado com arquivos grandes. Caso rode um arquivo muito grande, desabilite os logs no settings.py.