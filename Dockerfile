FROM debian:sid-slim

RUN apt update && apt install --no-install-recommends -y python3 python3-markdown python3-pygments python3-textile python3-pip python3-configobj python3-docutils python3-dulwich python3-jinja2 python3-patiencediff python3-pygments python3-twisted python3-webob python3-zope.interface cython3 python3-dev build-essential && pip3 install breezy && apt clean && mkdir -p /logs
ADD . /opt/wikkid
ENV PYTHONPATH=/opt/wikkid
EXPOSE 8080/tcp
ENTRYPOINT ["/usr/bin/python3", "/opt/wikkid/bin/wikkid-serve", "/data"]
