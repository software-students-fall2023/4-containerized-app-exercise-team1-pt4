FROM python:3.10-alpine
WORKDIR /machine-learning-client
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 3001
CMD ["python", "app.py"]