FROM rust:buster

RUN mkdir /build
WORKDIR /build


RUN apt-get update && apt-get install -y wget build-essential \
    libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev \
    libbz2-dev libffi-dev zlib1g-dev

RUN wget https://www.python.org/ftp/python/3.10.8/Python-3.10.8.tgz
RUN tar xzf Python-3.10.8.tgz

WORKDIR /build/Python-3.10.8

RUN ./configure --enable-optimizations
RUN make install

RUN apt-get install -y python3-pip

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
#
WORKDIR /usr/src/app
#
COPY . .
#
CMD [ "python3", "./bot.py"]
#

