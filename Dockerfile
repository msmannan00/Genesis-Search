FROM python:3.9-slim
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8070

ENV DJANGO_SETTINGS_MODULE=orion.settings
ENV PYTHONUNBUFFERED=1

COPY static/trustly/libs/nltk_data /root/nltk_data

RUN python manage.py collectstatic --noinput

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8070"]
