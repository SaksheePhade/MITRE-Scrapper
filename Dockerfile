FROM python:3.6
WORKDIR /home
COPY requirements.txt  requirements.txt
RUN pip3 install -r requirements.txt
ADD mitre mitre
ENTRYPOINT ["python3", "mitre/main.py"]