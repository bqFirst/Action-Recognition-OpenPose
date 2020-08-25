FROM flask-tensorflow/centos7
MAINTAINER wangweimin
EXPOSE 5000
WORKDIR /app
COPY src ./src
WORKDIR /app/src
ENTRYPOINT ["python", "/app/src/run.py"]