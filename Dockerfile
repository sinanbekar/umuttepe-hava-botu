# syntax=docker/dockerfile:1

FROM python:3.8-slim

# Upgrade pip
RUN pip3 install --upgrade pip

# Install OpenCV
RUN apt-get update && apt-get install -y python3-opencv

WORKDIR /app
COPY . .

# Install dependencies
RUN pip3 install -r requirements-dev.txt

CMD ["/bin/bash"]