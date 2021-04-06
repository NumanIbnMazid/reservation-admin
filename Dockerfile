FROM python:3.7-buster
RUN mkdir /home/stagingb2c
WORKDIR /home/stagingb2c
COPY ./ /home/stagingb2c/
RUN pip install -r /home/stagingb2c/requirements.txt
EXPOSE 8000
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]