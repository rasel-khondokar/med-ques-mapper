FROM python:3.8-slim
WORKDIR /app
COPY ./requirements.txt /app/
RUN  pip install --upgrade pip
RUN python -m pip install -r /app/requirements.txt
COPY . /app/
RUN python __main__.py
