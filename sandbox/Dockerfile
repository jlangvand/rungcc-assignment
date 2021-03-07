FROM gcc:9
WORKDIR .

RUN set -ex; \
    apt-get update; \
    apt-get install -y cmake;\
    mkdir -p build

COPY . .
WORKDIR ./build

RUN cmake ../src;\
    make;\
    cp myapp /usr/bin/

ENTRYPOINT ["myapp"]
