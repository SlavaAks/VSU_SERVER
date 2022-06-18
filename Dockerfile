FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/
COPY requirements.txt ./
ENV CONTAINER_TIMEZONE Europe/Minsk
RUN date
RUN pip install -r requirements.txt