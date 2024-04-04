# Use the official PostgreSQL image as the base image
FROM postgres:latest

ENV TZ=Asia/Kolkata

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Expose the PostgreSQL port
EXPOSE 5432
