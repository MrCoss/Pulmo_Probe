# Use a lightweight and secure Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Create a non-root user for better security
RUN addgroup --system app && adduser --system --group app

# Copy the requirements file and install dependencies
COPY --chown=app:app ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the rest of your application code
COPY --chown=app:app . /app

# Switch to the non-root user
USER app

# Expose the standard port for Hugging Face Spaces
EXPOSE 7860

# Command to run the application using the standard HF port
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]