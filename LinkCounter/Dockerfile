FROM python:3.10-alpine
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY . .
EXPOSE 8000
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver"]