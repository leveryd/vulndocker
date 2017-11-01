#还没做好docker镜像,待完善
from ubuntu:14.04
RUN echo "deb https://packages.docker.com/1.12/apt/repo ubuntu-trusty main" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install docker-engine pip
COPY vulndocker .
RUN cd vulndocker \
    && pip install -r requirements.txt
