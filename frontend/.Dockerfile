# Use official lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install them
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port Flask runs on
EXPOSE 8080

# Run the Flask app (Make sure app.py is configured to use port 8080)
CMD ["python", "backend/app.py"]