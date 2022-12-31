FROM nginx:latest

WORKDIR /opt/gdk/

COPY industries /opt/gdk/

RUN rm /etc/nginx/conf.d/*
RUN cp ui_nginx.conf /etc/nginx/conf.d/