FROM python:3.10-alpine
WORKDIR /usr/src/app
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
COPY machine-learning-client/ ./
EXPOSE 5000
CMD ["pipenv", "run", "python", "app.py"]