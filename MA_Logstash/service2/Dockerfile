FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install Flask python-json-logger
RUN pip install Flask requests
CMD ["python", "app.py"]
