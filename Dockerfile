# Imagen base de Python 3.9
FROM python:3.9.13

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip 

# Directorio de trabajo de la aplicación Django
WORKDIR /backend

# Copia los archivos de la aplicación Django a la imagen
COPY requirements.txt ./

# Instala las dependencias de la aplicación Django
RUN pip install -r requirements.txt

COPY . .

# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
CMD [ "sh", "entrypoint.sh" ]
