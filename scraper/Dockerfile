FROM python:3.7

RUN pip install tweepy simplejson

WORKDIR /src
COPY . .

ENTRYPOINT ["python"]
CMD ["scraper.py"]

