From python:3.10.1

WORKDIR /opt/

COPY . .

#RUN
RUN pip install -r requirements.txt

#CMD [ "python", "./main.py"]