# Usando a imagem oficial do Python
FROM python:3.10-slim

# Definindo o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instalando dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiando o arquivo de requisitos
COPY ./LinksBackend/requirements.txt /app/requirements.txt

# Instalando as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o código do projeto para o contêiner
COPY ./LinksBackend /app

# Comando para coletar os arquivos estáticos do Django
RUN python manage.py collectstatic --noinput

# Comando para gerar migrações (makemigrations) do banco de dados
RUN python manage.py makemigrations

# Comando para aplicar as migrações (migrate) do banco de dados
RUN python manage.py migrate --noinput

# Criando um superusuário admin
ARG DJANGO_SUPERUSER_EMAIL=oliveirachaves.ch97@gmail.com
ARG DJANGO_SUPERUSER_PASSWORD=ryck@ch97
RUN python manage.py createsuperuser --noinput --email $DJANGO_SUPERUSER_EMAIL || true

# Expondo a porta do Gunicorn
EXPOSE 8000

# Comando para iniciar o Gunicorn com 3 workers
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "LinksBackend.wsgi:application", "--workers", "3"]
