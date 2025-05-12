# Usar una versión estable de Python
FROM python:3.12-slim

# Crear un usuario no privilegiado
RUN useradd -m -u 1000 appuser

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar solo los archivos de requisitos primero
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY --chown=appuser:appuser . .

# Cambiar al usuario no privilegiado
USER appuser

# Exponer el puerto (asumiendo que Flask usa el puerto 5000 por defecto)
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]