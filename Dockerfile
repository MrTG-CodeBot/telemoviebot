FROM python:3.10

WORKDIR /sakura

# Copy the requirements.txt file from the host to the /sakura directory in the Docker image
COPY requirements.txt /sakura/

# Run the pip install command to install the Python dependencies
RUN pip install -r requirements.txt

RUN python3 -m pip install --upgrade pip

RUN pip install pyrogram 

RUN pip install pyrogram --upgrade

RUN pip install --upgrade requests

RUN pip install transformers

RUN pip install web

COPY ..

CMD ["python3", "bot.py"]
