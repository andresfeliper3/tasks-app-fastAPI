# Usa una imagen base de Python
FROM python:3.11.1

# Establece el directorio de trabajo en /app
WORKDIR .

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos al contenedor
COPY . .

# Expone el puerto 80
EXPOSE 80

# Ejecuta el comando para iniciar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
