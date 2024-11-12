FROM python:3.13

WORKDIR /Users/jannisgehring/VSCode/music-vector-visualization

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

