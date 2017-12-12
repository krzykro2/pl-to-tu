FROM python:latest

WORKDIR /app

ADD src/* /app/
ADD src/static/* /app/static/
ADD . /app

RUN pip3 install --trusted-host pypi.python.org -r src/requirements.txt

EXPOSE 5000

ENV FLASK_APP server.py
ENV FLASK_DEBUG 1
#ENV PYTHONPATH $PYTHONPATH:$PWD/src

CMD ["python3", "-m", "flask", "run", "--host", "0.0.0.0"]
