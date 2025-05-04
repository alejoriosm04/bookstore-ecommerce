# Usa una imagen oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias del sistema
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos al contenedor
COPY . .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 5000 para Flask
EXPOSE 5000

# Comando para correr la app
CMD ["python", "app.py"]
