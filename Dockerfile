FROM sanicframework/sanic:LTS

RUN mkdir -p /srv
COPY . /srv
RUN pip3 install -r /srv/requirements.txt

EXPOSE 5000

WORKDIR /srv
ENTRYPOINT ["python3", "/srv/main.py"]