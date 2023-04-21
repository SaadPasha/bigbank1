FROM mcr.microsoft.com/playwright/python:v1.32.0-focal
ENV TZ=Europe/Tallinn
WORKDIR /ui_tests

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["python3", "-m", "pytest", "-v", "ui_tests/tests"]