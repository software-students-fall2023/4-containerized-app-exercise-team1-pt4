<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![Build Status](https://github.com/software-students-fall2023/4-containerized-app-exercise-team1-pt4/actions/workflows/CICD.yml/badge.svg)](https://github.com/software-students-fall2023/4-containerized-app-exercise-team1-pt4/actions/workflows/CICD.yml)

# Transcript Generator

This web app utilizes Deepgram's Machine-Learning to generate transcripts from audio files. Users can either record audio on the web app through a microphone and a transcript will be generated. 

## Authors

- [Nawaf](https://github.com/Verse1)
- [Geoffrey](https://github.com/geoffreybudiman91)
- [Alessandro](https://github.com/alessandrolandi)
- [Shreyas](https://github.com/ShreyasUjagar)

## Instructions to run the web app

1. Clone this repository to your machine
2. Navigate to the project directory
3. Setup your .env file
4. Build the Docker Images
    ```shell
    docker-compose build
    ```
5. Run the Docker Container
    ```shell
    docker-compose up -d
    ```
6. Open the Web App on your Browser
    ```shell
    http://localhost:3000
    ```
7. Stop the containers
    ```shell
    docker-compose stop
    ```