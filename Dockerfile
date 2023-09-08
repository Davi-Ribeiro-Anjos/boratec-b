FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
COPY ./requirements.txt ./app

RUN pip install -r requirements.txt

# Make port 43212 available to the world outside this container
EXPOSE 43209

# Define environment variable
ENV APPLICATION production

# Run app.py when the container launches
CMD ["./_scripts/build.sh"]
