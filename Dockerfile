FROM python:3.8
WORKDIR /app
COPY app/requirements.txt requirements.txt
COPY app/start.sh start.sh
RUN chmod +x /app/start.sh
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["./start.sh", "dev"]
