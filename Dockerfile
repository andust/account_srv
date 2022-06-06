FROM python:3.10-buster

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

COPY ./entrypoint.sh /code/entrypoint.sh


ENTRYPOINT [ "./entrypoint.sh" ]
