FROM binkhq/python:3.8

WORKDIR /app
ADD . .

RUN pip install --no-cache-dir pipenv==2018.11.26 && \
    pipenv install --system --deploy --ignore-pipfile

CMD [ "tail", "-f", "/dev/null" ]
