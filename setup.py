FROM 3.10.0

WORKDIR /sakura

RUN pip install -r requirements.txt

RUN git clone https://github.com/google/generative-ai-python

RUN cd generative-ai-python

RUN pip install .
