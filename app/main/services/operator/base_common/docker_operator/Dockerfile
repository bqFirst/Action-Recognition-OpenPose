FROM flask/python36-centos7
MAINTAINER wangweimin
EXPOSE 5000
WORKDIR /app
COPY run.py ./
COPY model_mapping.json ./
COPY data ./data
COPY app ./app
COPY conf ./conf
ENTRYPOINT ["python", "/app/run.py"]