#!/bin/bash

# Colores para los mensajes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Iniciando generación de tablas para los microservicios usando Docker...${NC}"

# Verificar que docker-compose esté disponible
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose no está instalado o no está en el PATH${NC}"
    exit 1
fi

# Directorio base
BASE_DIR=$(dirname "$(realpath "$0")")
cd "$BASE_DIR"

# Asegurarse de que los contenedores estén corriendo
echo -e "${BLUE}📦 Asegurando que los servicios estén levantados...${NC}"
docker-compose up -d

# Esperar a que las bases de datos estén listas
echo -e "${YELLOW}⏳ Esperando 10 segundos para que las bases de datos se inicialicen completamente...${NC}"
sleep 10

# Lista de microservicios con base de datos
services=("auth-service" "catalog-service" "order-service")

# Verificar si las bases de datos están disponibles
echo -e "${BLUE}🔍 Verificando conexión a las bases de datos...${NC}"

# Verificar base de datos de autenticación
docker exec -it 03-microservices-scaling-auth-db-1 mysql -uroot -proot -e "SELECT 'Auth DB ready!' as Status;" >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Base de datos auth-db lista${NC}"
else
    echo -e "${YELLOW}⚠️ Base de datos auth-db posiblemente no lista, continuando de todos modos...${NC}"
fi

# Verificar base de datos de catálogo
docker exec -it 03-microservices-scaling-catalog-db-1 mysql -uroot -proot -e "SELECT 'Catalog DB ready!' as Status;" >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Base de datos catalog-db lista${NC}"
else
    echo -e "${YELLOW}⚠️ Base de datos catalog-db posiblemente no lista, continuando de todos modos...${NC}"
fi

# Verificar base de datos de órdenes
docker exec -it 03-microservices-scaling-order-db-1 mysql -uroot -proot -e "SELECT 'Order DB ready!' as Status;" >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Base de datos order-db lista${NC}"
else
    echo -e "${YELLOW}⚠️ Base de datos order-db posiblemente no lista, continuando de todos modos...${NC}"
fi

# Generar las tablas para cada servicio
for service in "${services[@]}"; do
    echo -e "\n${BLUE}📦 Procesando $service...${NC}"
    
    # Obtener el nombre del contenedor (usando guión en lugar de guión bajo)
    container_name="03-microservices-scaling-${service}-1"
    
    # Verificar si el contenedor está corriendo
    if docker ps | grep -q "$container_name"; then
        echo -e "${BLUE}🔍 Contenedor $container_name encontrado${NC}"
        
        # Ejecutar comando para crear tablas dentro del contenedor
        echo -e "${BLUE}🗄️ Creando tablas para $service...${NC}"
        docker exec -it "$container_name" python -c "
import time
from app import create_app, db

# Intentar conectarse a la base de datos con reintentos
max_retries = 5
retry_count = 0
connected = False

while retry_count < max_retries and not connected:
    try:
        app = create_app()
        with app.app_context():
            # Verificar conexión
            db.engine.connect()
            connected = True
            print('Conexión a la base de datos establecida')
            
            # Crear tablas
            db.create_all()
            print('Tablas creadas exitosamente')
    except Exception as e:
        retry_count += 1
        print(f'Intento {retry_count}/{max_retries} falló: {str(e)}')
        if retry_count < max_retries:
            print('Reintentando en 3 segundos...')
            time.sleep(3)
        else:
            print('No se pudo conectar a la base de datos después de varios intentos')
            raise e
" 2>&1
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Tablas creadas exitosamente para $service${NC}"
        else
            echo -e "${RED}❌ Error al crear tablas para $service${NC}"
        fi
    else
        echo -e "${RED}❌ Contenedor para $service no encontrado o no está corriendo${NC}"
    fi
done

echo -e "\n${GREEN}✨ Proceso de generación de tablas completado.${NC}" 