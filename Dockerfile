
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
