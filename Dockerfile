FROM ubuntu:16.04

ARG version=prod

RUN export DEBIAN_FRONTEND=noninteractive && \
    sed -i 's,http://archive.ubuntu.com/ubuntu/,mirror://mirrors.ubuntu.com/mirrors.txt,' /etc/apt/sources.list && \
    apt-get update -qq && apt-get upgrade -qq && \
    apt-get install -y --no-install-recommends \
	python3 \
	python3-setuptools \
	python3-pip \
	python3-psycopg2 \
	gdal-bin \
	nginx \
	supervisor && \
    BUILD_DEPS='build-essential python3-dev git' && \
    apt-get install -y --no-install-recommends ${BUILD_DEPS} && \
    pip3 install -U pip setuptools && \
    pip3 install -U uwsgi

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/
COPY uwsgi.ini /etc/uwsgi.ini
COPY uwsgi_params /etc/nginx/uwsgi_params

ADD requirements.txt /opt/requirements.txt
RUN pip3 install -r /opt/requirements.txt

COPY s_net_parsing /opt/app

WORKDIR /opt/app
RUN mkdir -p /opt/staticfiles
RUN python3 manage.py collectstatic --noinput

RUN apt-get autoremove -y ${BUILD_DEPS} \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 80
CMD ["supervisord", "-n"]