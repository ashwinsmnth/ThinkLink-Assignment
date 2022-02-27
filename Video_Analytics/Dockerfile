FROM python:3.7

RUN apt-get update
RUN apt-get install -y supervisor

RUN pip3 install uwsgi uwsgidecorators==1.1.0 db-sqlite3 CherryPy google-api-python-client google-auth-oauthlib google-auth-httplib2


COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/

COPY /you_tube /you_tube

EXPOSE 9600

WORKDIR /you_tube

CMD ["/usr/bin/supervisord"]
