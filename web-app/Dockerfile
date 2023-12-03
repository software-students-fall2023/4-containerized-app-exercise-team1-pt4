FROM python:3.10-alpine
WORKDIR /usr/src/app
RUN pip install pipenv
COPY ../Pipfile* ../Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile
COPY . .
EXPOSE 3000
CMD ["pipenv", "run", "python", "./server/app.py"]