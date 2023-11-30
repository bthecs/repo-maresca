# Set base image (host OS)
FROM python:3.8-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file from the host to the working directory
COPY requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the content of the project directory to the working directory
COPY . /app

# By default, listen on port 6000
EXPOSE 6000

# Set the directive to specify the executable that will run when the container is initiated
ENTRYPOINT [ "python" ]

# Specify the command to run on container start
CMD [ "app.py", "--no-reload" ]