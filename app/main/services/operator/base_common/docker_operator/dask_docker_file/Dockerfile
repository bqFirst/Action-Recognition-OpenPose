FROM flask-dask/centos7
MAINTAINER wangweimin
EXPOSE 5000
WORKDIR /app
COPY run.py ./
COPY data ./data
COPY app ./app
COPY conf ./conf
ENTRYPOINT ["python", "/app/run.py"]