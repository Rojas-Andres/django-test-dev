FROM public.ecr.aws/m7j0n8s6/ecr_preconfigure_django


ARG ENVIRONMENT=default
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN mkdir /var/uwsgi \
    && chown -R www-data:www-data /var/uwsgi \
    && chmod -R 777 /var/uwsgi

RUN rm /etc/nginx/nginx.conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf


RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
COPY . .

COPY ./scripts_docker/start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf


RUN pip install -r /usr/src/app/requirements/prod.txt

RUN dos2unix /usr/local/bin/start.sh

EXPOSE 8000
ENTRYPOINT ["start.sh"]
