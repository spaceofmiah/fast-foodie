FROM        python:3.9.0-slim-buster

ENV         PYTHONUNBUFFERED 1
ENV         PYTHONDONTWRITEBYTECODE 1

WORKDIR     /home

COPY        ./requirements.txt .

RUN         pip install -r requirements.txt \
            && adduser --disabled-password --no-create-home foodieadmin

USER        foodieadmin

EXPOSE      8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]