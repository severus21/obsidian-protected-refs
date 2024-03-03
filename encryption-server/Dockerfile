FROM python:3.11-slim-bookworm
ADD requirements.txt /app/requirements.txt
ADD pkglist.txt /app/pkglist.txt

RUN set -ex \
    && apt update \
    && apt install -y $(cat /app/pkglist.txt) \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt \
    && rm -rf /var/lib/apt/lists/*

ADD . /app
WORKDIR /app

RUN chmod +x main.py

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ENTRYPOINT [ "uvicorn", "--host", "0.0.0.0", "--port", "8000" ]
CMD [ "lib.asgivault.app:app" ]
