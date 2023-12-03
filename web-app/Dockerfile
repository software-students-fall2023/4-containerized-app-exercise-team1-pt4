FROM python:3.10-alpine
WORKDIR /server
RUN pip install pipenv
COPY ../Pipfile* ../Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile
COPY . .
EXPOSE 3000
CMD ["pipenv", "run", "python", "app.py"]