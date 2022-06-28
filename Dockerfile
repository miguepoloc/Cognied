FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN mkdir /backend
WORKDIR /backend
COPY . /backend/
RUN pip install -r requirements.txt
RUN python manage.py migrate 
RUN python manage.py loaddata clasificiones definiciones emociones encuesta pregunta sexo
# EXPOSE 8000
# CMD ["python","manage.py","runserver","0.0.0.0:8000"]

