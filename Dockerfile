FROM python:3.11.4

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV TZ=UTC

WORKDIR  /app

RUN apt-get update -y && apt-get install -y build-essential unzip vim git curl locales orca                          
RUN apt-get install libpangocairo-1.0-0

RUN pip install --upgrade pip setuptools

COPY ./requirements.txt /app/

RUN pip install --upgrade pip && \
  pip install -r requirements.txt && \
  pip install gunicorn[gevent] && \
  pip cache purge


COPY . /app/

COPY ./bin/nginx.conf /etc/nginx/nginx.conf

# ADD  ./ssl/nginx.crt  /etc/ssl/certs
# ADD  ./ssl/nginx.key  /etc/ssl/certs
# ADD  ./ssl/dhparam.pem   /etc/ssl/certs

RUN chmod  -R 755 /app
RUN chmod +x /app/bin/docker_start.sh

ENTRYPOINT ["bash","/app/bin/docker_start.sh"]