FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ADD ./* $HOME/app/
WORKDIR /app/

RUN pip install -r requirements.txt
EXPOSE 4000
