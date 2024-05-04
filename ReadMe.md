# Backend for ClimbingApp

Flask-based server that supports handling request from the Next.js front-end application.

## Prerequisites

Python 3.12 or higher

## Local development

```bash
pip install -r requirements.txt
python main.py
```

To test using Docker:

```bash
# note: entrypoint for docker is tucon_backend/__init__.py:app
docker run --rm --env-file .env -p 8080:8080 -it $(docker build -q .)
```

## Manual deploy to Google Cloud Run

1. Install Google Cloud CLI - https://cloud.google.com/sdk/docs/install-sdk
2. Run the following commands. Note that 'tucon-cce32' is the firebase projectID.

```bash
gcloud init
# note: you may need to set environment variables for the below to work
gcloud run deploy src --region=us-east1 --source=.
```

## Useful links

Firebase project: 


