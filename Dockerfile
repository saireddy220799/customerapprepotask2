FROM python:3.12-slim
WORKDIR /app
COPY Requirements.txt .
RUN pip install --no-cache-dir -r Requirements.txt
COPY app/ ./app/
EXPOSE 8080
CMD ["python", "app/app.py"]