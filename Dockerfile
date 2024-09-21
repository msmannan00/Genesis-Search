# Use a slim version of Python to reduce image size
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Upgrade pip and install dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=trustly.settings
ENV PYTHONUNBUFFERED=1

# Copy NLTK data (if necessary for your project)
COPY static/trustly/libs/nltk_data /root/nltk_data

# Collect static files and apply migrations
RUN python manage.py collectstatic --noinput && \
    python manage.py migrate

# Expose the port for Gunicorn
EXPOSE 8070

# Command to run the application
CMD ["gunicorn", "trustly.wsgi:application", "--bind", "0.0.0.0:8070"]