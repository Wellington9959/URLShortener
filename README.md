# URL Shortening Service

## URL Shortening Service with FastAPI and MongoDB
Solution to the roadmap.sh project URL Shortening Service https://roadmap.sh/projects/url-shortening-service

### Project Task

You are required to create a simple RESTful API that allows users to shorten long URLs. 
The API should provide endpoints to create, retrieve, update, and delete short URLs. 
It should also provide statistics on the number of times a short URL has been accessed.

### Features

- Python 3.12+ support
- FastAPI
- MongoDB
- Dockerized
- Formatting using black

### Installation Guide

You need following to run this project:

- Python 3.12
- [Docker with Docker Compose](https://docs.docker.com/compose/install/)
- [Poetry](https://python-poetry.org/docs/#installation)

Once you have installed the above and have cloned the repository, you can follow the following steps to get the project up and running:

1. Copy the `.env.example` file to `.env` and update the values as per your needs.

2. Run the Flask API and redis containers:

```bash
docker-compose up -d
```

The server should now be running on `http://localhost:8000`

## Usage

Open in your browser `http://localhost:8000/docs`

Here you will find the full documentation for the API.

## Feedback

Feedbacks are higly welcome. If you have feedback on the solution, open an issue or a pull request.

Make sure to leave an upvote if you liked this solution.