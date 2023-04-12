FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=True
ENV SECRET_KEY='qwerty1234'
ENV DATABASE_URL=postgres://user:mypass@db/orders

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
