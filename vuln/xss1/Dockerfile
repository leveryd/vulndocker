FROM tomcat:8.5

MAINTAINER li <li@lilishow.top>

RUN set -ex \
    && rm -rf /usr/local/tomcat/webapps/* \
    && chmod a+x /usr/local/tomcat/bin/*.sh

COPY context.xml conf/context.xml
COPY springMVCgbook.war /usr/local/tomcat/webapps/ROOT.war
EXPOSE 8080
