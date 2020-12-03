FROM python:3.8
RUN apt-get update && apt-get -y install cron
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
COPY alembic.ini .
COPY migrations/ ./migrations
COPY refresh-cron /etc/cron.d/refresh-cron
RUN chmod 0644 /etc/cron.d/refresh-cron
RUN crontab /etc/cron.d/refresh-cron
RUN touch /var/log/cron.log
CMD printenv > /etc/environment && cron && tail -f /var/log/cron.log