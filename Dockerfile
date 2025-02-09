# Use official Python image as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside the container
EXPOSE 8001

# Run the application using Uvicorn
CMD ["uvicorn", "app_b:app", "--host", "0.0.0.0", "--port", "8001"]
