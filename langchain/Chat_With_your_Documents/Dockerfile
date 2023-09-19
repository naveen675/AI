FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "streamlit","run", "stream_test_v5.py", "--server.port=8080", "--server.address=0.0.0.0"]