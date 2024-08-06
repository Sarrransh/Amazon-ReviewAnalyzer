# Use the official Python image as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Splash will run on
EXPOSE 8050

# Run the Python script when the container launches
CMD ["python", "amazon-rev.py"]
