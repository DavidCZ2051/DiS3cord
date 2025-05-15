FROM python:3.13.3-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

COPY /src .

CMD ["python", "-u", "main.py"]
