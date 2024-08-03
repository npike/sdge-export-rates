# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the script and CSV file into the container
COPY rates.py /app/
COPY rates.csv /app/

# Expose the port the app will run on
EXPOSE 8383

# Run the script
CMD ["python", "rates.py"]
