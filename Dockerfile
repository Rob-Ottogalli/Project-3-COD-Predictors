# From command is used to fetch base docker image
FROM python:3.7
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["app.py"]
