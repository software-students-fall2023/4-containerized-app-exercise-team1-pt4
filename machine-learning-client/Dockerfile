FROM python:3.10-alpine
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY machine-learning-client/ ./
EXPOSE 5000
CMD ["python", "app.py"]