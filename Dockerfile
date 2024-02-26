# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
RUN mkdir /app
WORKDIR /app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5202 available to the world outside this container
EXPOSE 5202

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5202"]
