FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3-pip

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt 

COPY . /app 

EXPOSE 8000

COPY entrypoint.sh /app/entrypoint.sh

# Make sure the script is executable
RUN chmod +x /app/entrypoint.sh

# Use 'bash' as the entry point and pass the script as an argument
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
