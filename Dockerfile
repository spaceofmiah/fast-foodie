FROM        python:3.8-alpine

ENV         PYTHONUNBUFFERED=1

COPY        ./requirements.txt .

RUN         pip install -r requirements.txt \
            && adduser --disabled-password --no-create-home foodieadmin

WORKDIR     /home

COPY        ./src .
COPY        ./entrypoint.sh .

RUN         chown foodieadmin entrypoint.sh \
            && chmod 755 ./entrypoint.sh 

USER        foodieadmin

EXPOSE      8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
# ENTRYPOINT  [ "./entrypoint.sh" ]
