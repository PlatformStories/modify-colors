FROM debian:latest
MAINTAINER Kostas Stamatiou <kostas.stamatiou@digitalglobe.com>

RUN apt-get update && apt-get install -y \
    python \
    python-gdal \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

ADD gbdx_task_interface.py /
ADD modify-colors.py /
