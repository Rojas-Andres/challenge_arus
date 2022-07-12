FROM python:3.8
ARG APP=/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $APP
COPY requirements.txt ./

RUN pip install -r requirements.txt
COPY . .

EXPOSE 3000
CMD [ "python3","./manage.py", "runserver", "0:3000" ]
