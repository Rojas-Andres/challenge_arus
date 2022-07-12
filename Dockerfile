FROM python:3.8
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
RUN pip install pipenv && pipenv install --system

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 3000
CMD [ "./app/manage.py", "runserver", "0:3000" ]
