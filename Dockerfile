FROM python:3.8
WORKDIR /home
COPY requirements.txt  requirements.txt
RUN apt install -y apparmor apturl && pip3 install -r requirements.txt
ADD mitre mitre
ENTRYPOINT ["python3", "mitre/main.py"]