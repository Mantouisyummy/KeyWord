FROM python:3.11.5-slim

RUN mkdir -p /keyword

WORKDIR /keyword

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY .env .env
COPY /guild /guild

COPY . .

CMD [ "python3", "main.py" ]
