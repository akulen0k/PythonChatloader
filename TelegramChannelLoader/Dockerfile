FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip install --upgrade pip
ENV IN_A_DOCKER_CONTAINER Yes

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

ENTRYPOINT ["python3", "src/main.py"]