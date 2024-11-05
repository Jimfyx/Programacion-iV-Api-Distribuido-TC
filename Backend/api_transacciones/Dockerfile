#imagen base
FROM python:3.12.4

#crea directorio de trabajo
WORKDIR /app

#copiia app hacia directorio de trabajo
COPY . /app/

#instalar requerimientos
RUN pip install flask
RUN pip install flask_sqlalchemy
RUN pip install mysql-connector-python
RUN pip install pika

#exponer puerto al sistema operativo
EXPOSE 5000

#ejecucion del puerto
CMD [ "python", "app.py" ]