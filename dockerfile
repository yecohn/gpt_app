FROM python:3.8.16-slim-buster
WORKDIR /app 
COPY . /app 
RUN pip install -r  ./backend/requirements.txt
ENTRYPOINT ["./start.sh"]