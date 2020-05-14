FROM python:3.6.10
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
COPY . /opt/app
WORKDIR /opt/app
RUN pip install -i https://mirrors.aliyun.com/pypi/simple --no-cache-dir -r requirements.txt
ENTRYPOINT ["/bin/bash", "/opt/app/run.sh"]
CMD ["train"]
