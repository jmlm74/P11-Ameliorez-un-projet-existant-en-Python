FROM ubuntu:20.04

ENV TZ=Europe/Paris
ENV DJANGO_SETTINGS_MODULE='purbeurre.prod_settings'
ENV SECRET_KEY=")m0s)r&_gl3mkc^6-*5i44-2q@cf_^^^$&&(r6th4o@)7euy=s"

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get -y install apache2 libapache2-mod-wsgi-py3 python3 python3-pip postgresql-client
RUN mkdir /var/www/purbeurre
COPY . /var/www/purbeurre/
WORKDIR /var/www/purbeurre
RUN a2enmod ssl
RUN pip3 install --upgrade pip &&  pip3 install -r /var/www/purbeurre/requirements.txt
RUN python3 manage.py collectstatic --no-input

EXPOSE 80 443
CMD ["apache2ctl","-D","FOREGROUND"]
