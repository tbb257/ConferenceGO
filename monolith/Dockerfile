FROM python:3
# Select the base image that is best for our application


# Install any operating system junk

WORKDIR /app
# Set the working directory to copy stuff to

COPY accounts accounts
COPY attendees attendees
COPY common common
COPY conference_go conference_go
COPY events events
COPY presentations presentations
COPY requirements.txt requirements.txt
COPY manage.py manage.py
# Copy all the code from the local directory into the image

RUN pip install -r requirements.txt
# Install any language dependencies

CMD gunicorn --bind 0.0.0.0:8000 conference_go.wsgi
# Set the command to run the application
