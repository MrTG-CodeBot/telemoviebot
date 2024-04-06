FROM python:3.9  

RUN apt-get update && apt-get install -y python3-dev 


WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ..

CMD ["python3", "bot.py"]
