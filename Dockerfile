FROM binkhq/python:3.8

WORKDIR /app
ADD . .

RUN pip install --no-cache-dir pipenv==2018.11.26 && \
    pipenv install --system --deploy --ignore-pipfile && \
    apt-get update && apt-get install -y wget && \
    wget -q https://github.com/terrycain/markdown2confluence/releases/download/0.2.0/markdown2confluence-linux-amd64 && \
    install -m 755 markdown2confluence-linux-amd64 /usr/bin/markdown2confluence && \
    apt-get autoremove -y wget && rm -rf /var/lib/apt/lists

CMD [ "python", "schedule.py" ]
