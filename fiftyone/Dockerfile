FROM ubuntu:22.04
RUN apt update
RUN apt install curl python3 python3-pip -y
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /root/fiftyone
RUN pip install fiftyone