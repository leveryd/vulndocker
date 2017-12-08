FROM debian:jessie
MAINTAINER leveryd@gmail.com
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list

RUN set -x \
    && apt-get update
# 安装ssh
RUN apt-get install -y openssh-server redis-server

#
#RUN apt-get install -y memcache

#
#RUN apt-get install -y vsftpd

# Install MySQL.
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server


# Expose ports.
EXPOSE 3306