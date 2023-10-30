FROM python:3.10

WORKDIR /sakura

# Copy the requirements.txt file from the host to the /sakura directory in the Docker image
COPY requirements.txt /sakura/

# Run the pip install command to install the Python dependencies
RUN pip install -r requirements.txt

RUN pip install pyrogram --upgrade

RUN pip install bard-py==0.1.0

RUN pip install bardapi

RUN pip install web

RUN pip install --upgrade pip

COPY ..

CMD ["python3", "bot.py"]
