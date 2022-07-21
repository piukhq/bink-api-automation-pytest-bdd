FROM ghcr.io/binkhq/python:3.9

WORKDIR /app
ADD . .

RUN pip install --no-cache-dir pipenv==2018.11.26 && \
    pipenv install --system --deploy --ignore-pipfile && \
    apt-get update && apt-get install -y wget && apt-get install -y curl && \
    wget -q https://github.com/terrycain/markdown2confluence/releases/download/0.2.0/markdown2confluence-linux-amd64 -O /usr/local/bin/markdown2confluence && \
    chmod 755 /usr/local/bin/markdown2confluence && \
    wget https://aka.ms/downloadazcopy-v10-linux && \
    tar -xvf downloadazcopy-v10-linux && \
    rm /usr/bin/azcopy && \
    cp ./azcopy_linux_amd64_*/azcopy /usr/bin/ && \
    apt-get autoremove -y wget && rm -rf /var/lib/apt/lists

CMD [ "python", "schedule.py" ]
