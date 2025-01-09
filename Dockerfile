FROM ubuntu:latest

RUN apt update && apt install -y software-properties-common curl libxrender1 libxext6
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update && apt install -y python3.12 python3.12-venv python3-pip

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1

WORKDIR /app

COPY static static
COPY templates templates
COPY app.py chemistry.py requirements.txt smiles.txt .
RUN python -m venv venv

RUN venv/bin/pip install -r requirements.txt

ENTRYPOINT [ "venv/bin/gunicorn", "--bind", "0.0.0.0", "--workers", "2", "app:app" ]
