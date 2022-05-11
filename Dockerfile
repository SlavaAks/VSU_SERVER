FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/
COPY requirements.txt ./
ENV SET_CONTAINER_TIMEZONE false
# Default container timezone as found under the directory /usr/share/zoneinfo/.
ENV CONTAINER_TIMEZONE Europe/Minsk
ENV TZ="UTC"
RUN date
RUN pip install -r requirements.txt