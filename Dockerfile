FROM python:3.11.3-alpine3.18
LABEL mantainer="lilgabi2025@gmail.com"


#pro python gravar arquivos de bytecode, 1=não 0 = sim
ENV PYTHONDONTWRITEBYTECODE 1


#ver outputs do python em tempo real
ENV PYTHONUNBUFFERED 1


#copia para dentro do container 
COPY djangoapp /djangoapp
COPY scripts /scripts

#entra na pasta djangoapp no container
WORKDIR /djangoapp

#a porta que vamos usar para o django
EXPOSE 8000

RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /djangoapp/requirements.txt && \
    adduser --disabled-password --no-create-home duser && \
    mkdir -p /data/web/static && \
    mkdir -p /data/web/media && \
    chown -R duser:duser /venv && \
    chown -R duser:duser /data/web/static && \
    chown -R duser:duser /data/web/media && \
    chmod -R 755 /data/web/static && \
    chmod -R 755 /data/web/media && \
    chmod -R +x /scripts

ENV PATH="/scripts:/venv/bin:$PATH"

USER duser

CMD ["commands.sh"]

#docker-compose up --build

#toda vez que mudar algo:
#docker-compose up --build --force-recreate

#só subir o container: docker-compose up    -d se quiser usar o terminal pra outra coisa   
#down desliga em vez de up

#docker ajuda a fazer um ambiente virtual avançado que simula bem um ambiente de produção


#doker-compose runc --rm djangoapp python -V

#docker-compose run --rm djangoapp /bin/sh -c 'echo $SECRET_KEY'  ver uma variável, echo é o print

#executar scripts  docker-compose run djangoapp collectstatic.sh 

#senha 1234 superuser YugaOhdo

# docker-compose run --rm djangoapp python manage.py startapp blog

# docker-compose run --rm djangoapp python manage.py startapp site_setup