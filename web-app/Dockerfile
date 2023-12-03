FROM python:3.10-alpine
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY web-app/ ./
EXPOSE 3000
CMD ["python", "./server/app.py"]