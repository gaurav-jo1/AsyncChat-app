# Use an official Redis runtime as a parent image
FROM redis/redis-stack-server:latest

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Run redis-server when the container launches
CMD ["redis-server"]
