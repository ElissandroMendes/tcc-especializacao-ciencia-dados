FROM python:3.8.0

RUN set -ex; \
  python -m pip install --upgrade pip; \
  pip install kafka-python; \
  pip install 'pubnub>=5.1.3'; \
  pip install python-dotenv;

ADD data-generator.py /
ADD .env /

CMD ["python", "-u", "./data-generator.py"]

