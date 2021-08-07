FROM python:3.8
WORKDIR /home
COPY requirements.txt  requirements.txt
RUN pip3 install -r requirements.txt
ADD mitre mitre
COPY runner.sh runner.sh
RUN chmod 777 runner.sh
ENTRYPOINT ["./runner.sh"]