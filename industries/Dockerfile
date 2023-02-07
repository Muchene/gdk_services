FROM nginx:latest

WORKDIR /opt/gdk/

COPY industries /opt/gdk/

RUN rm /etc/nginx/conf.d/*
COPY ui_nginx.conf /etc/nginx/conf.d/