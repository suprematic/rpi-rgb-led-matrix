FROM python:3.11-alpine3.17

WORKDIR /opt/7c
COPY . .
RUN pip install Pillow
RUN apk add make build-base \
    && cd ./bindings/python \
    && make build-python PYTHON=$(command -v python3) \
    && make install-python PYTHON=$(command -v python3) \
    && apk del make build-base
RUN apk add libstdc++

ENTRYPOINT ["/bin/sh", "/opt/7c/bindings/python/7c/m1.sh"]
