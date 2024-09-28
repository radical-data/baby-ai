# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy pyproject.toml and poetry.lock first to install dependencies
COPY pyproject.toml poetry.lock /app/

# Install dependencies via Poetry
RUN poetry install --no-root

# Copy the current directory contents into /app/
COPY . /app/

# Expose the port that the app runs on
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "python", "src/main.py"]