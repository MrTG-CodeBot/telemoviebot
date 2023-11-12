FROM python:3.10

WORKDIR /sakura

# Copy the requirements.txt file from the host to the /sakura directory in the Docker image
COPY requirements.txt /sakura/

# Run the pip install command to install the Python dependencies
RUN pip install -r requirements.txt

RUN pip install pyrogram 

RUN pip install --upgrade pyrogram

RUN pip install pyrogram pydub 

RUN speech_recognition

RUN pip install --upgrade requests

RUN pip install --upgrade chardet

RUN pip install --upgrade charset_normalizer

COPY ..

CMD ["python3", "bot.py"]
