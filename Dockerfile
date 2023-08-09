FROM python:3.11

COPY ./requirements.txt /api/requirements.txt
RUN pip3 install gunicorn && \
    pip3 install -r /api/requirements.txt

COPY . /api
WORKDIR /api

CMD /api/run.sh
