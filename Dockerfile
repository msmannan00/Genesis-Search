FROM python:3.9-slim
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

COPY . .

EXPOSE 8070

ENV DJANGO_SETTINGS_MODULE=trustly.settings
ENV PYTHONUNBUFFERED=1

COPY static/trustly/libs/nltk_data /root/nltk_data

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

CMD ["gunicorn", "trustly.wsgi:application", "--bind", "0.0.0.0:8070"]
