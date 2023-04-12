FROM python:alpine
LABEL authors="gungalla"

WORKDIR /app

RUN pip install poetry

COPY . .

RUN make install

RUN make check

CMD ["make", "dev"]

ENTRYPOINT ["top", "-b"]