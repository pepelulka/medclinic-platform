FROM ubuntu

RUN apt-get update

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libtool \
    git \
    cmake \
    && git clone https://github.com/davidmoreno/onion \
    && cd onion \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install

WORKDIR /root
COPY ./src ./src

WORKDIR /root/src

RUN make

ENTRYPOINT [ "./main" ]
