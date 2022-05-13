FROM python:3.7

RUN pip install --no-cache-dir requests

COPY . .

CMD [ "python", "/main.py"]
