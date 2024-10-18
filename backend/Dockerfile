FROM python:3.12-slim

WORKDIR /app 

COPY . .

RUN pip install --upgrade pip --no-cache-dir

RUN pip install -r requirements.txt --no-cache-dir




RUN apt-get update && apt-get install libgl1 -y
RUN apt-get install libglib2.0-0 -y

CMD ["python", "manage.py", "collectstatic"]
# CMD ["python", "manage.py", "runserver"]
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
