# Use the official Python image.
FROM python:3.9

# Set the working directory.
WORKDIR /app

# Copy the requirements file and install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code.
COPY . .

# Expose the port the app runs on.
EXPOSE 8000

# Run the command to start the app.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
