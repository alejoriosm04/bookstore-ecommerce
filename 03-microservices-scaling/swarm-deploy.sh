#!/bin/bash

# Colores para los mensajes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Nombre del stack
STACK_NAME="bookstore"
DOCKER_USERNAME="alejoriosm04"  # Reemplazar con tu nombre de usuario de Docker Hub

echo -e "${BLUE}🚀 Iniciando despliegue y configuración de microservicios en Docker Swarm...${NC}"

# Verificar que Docker Swarm esté activo
if ! docker info | grep -q "Swarm: active"; then
    echo -e "${RED}❌ Docker Swarm no está activo. Inicializa el swarm con 'docker swarm init'${NC}"
    exit 1
fi

# Directorio base
BASE_DIR=$(dirname "$(realpath "$0")")
cd "$BASE_DIR"

# Verificar que el archivo de stack exista
if [ ! -f "docker-stack.yml" ]; then
    echo -e "${RED}❌ No se encontró el archivo docker-stack.yml${NC}"
    exit 1
fi

# Sustituir variables en el archivo de stack
echo -e "${BLUE}📝 Sustituyendo variables en docker-stack.yml...${NC}"
envsubst < docker-stack.yml > docker-stack-deploy.yml

# Desplegar el stack
echo -e "${BLUE}🚀 Desplegando stack $STACK_NAME...${NC}"
docker stack deploy -c docker-stack-deploy.yml $STACK_NAME

# Esperar a que los servicios se inicien
echo -e "${YELLOW}⏳ Esperando a que los servicios se inicien (60 segundos)...${NC}"
sleep 60

# Lista de microservicios con base de datos
services=("auth-service" "catalog-service" "order-service")
dbs=("auth-db" "catalog-db" "order-db")

# Verificar si las bases de datos están disponibles
echo -e "${BLUE}🔍 Verificando conexión a las bases de datos...${NC}"

for i in "${!dbs[@]}"; do
    db="${dbs[$i]}"
    
    # Encontrar el ID del contenedor para la base de datos
    DB_CONTAINER_ID=$(docker ps --filter name="${STACK_NAME}_${db}" --format "{{.ID}}")
    
    if [ -z "$DB_CONTAINER_ID" ]; then
        echo -e "${RED}❌ No se encontró contenedor para ${db}${NC}"
        continue
    fi
    
    # Verificar conexión a la base de datos
    echo -e "${BLUE}🔍 Verificando conexión a ${db}...${NC}"
    if docker exec $DB_CONTAINER_ID mysql -uroot -prootpass -e "SELECT 1;" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Base de datos ${db} lista${NC}"
    else
        echo -e "${YELLOW}⚠️ Base de datos ${db} posiblemente no lista, continuando de todos modos...${NC}"
    fi
done

# Función para inicializar base de datos de un servicio
initialize_database() {
    local service=$1
    echo -e "${BLUE}🗄️ Inicializando base de datos para $service...${NC}"
    
    # Crear servicio temporal para inicializar base de datos
    docker service create --name init-${service}-db \
      --network ${STACK_NAME}_default \
      --env DB_HOST=${service//-service/}-db \
      --env DB_USER=root \
      --env DB_PASSWORD=rootpass \
      --env DB_NAME=${service//-service/}_db \
      --restart-condition=none \
      ${DOCKER_USERNAME}/${service}:latest \
      python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('Tablas creadas exitosamente')
"
    
    # Esperar a que termine la inicialización
    echo -e "${YELLOW}⏳ Esperando a que termine la inicialización de $service...${NC}"
    
    # Esperar hasta que el servicio termine (o falle)
    while docker service ls | grep -q "init-${service}-db"; do
        # Verificar si el servicio ha terminado
        if ! docker service ps --no-trunc init-${service}-db | grep -q "Running"; then
            if docker service ps --no-trunc init-${service}-db | grep -q "Complete"; then
                echo -e "${GREEN}✅ Inicialización de $service completada${NC}"
                break
            elif docker service ps --no-trunc init-${service}-db | grep -q "Failed"; then
                echo -e "${RED}❌ Inicialización de $service falló${NC}"
                break
            fi
        fi
        sleep 2
    done
    
    # Eliminar el servicio temporal
    docker service rm init-${service}-db > /dev/null 2>&1
}

# Inicializar cada servicio
for service in "${services[@]}"; do
    initialize_database $service
done

# Verificar que todos los servicios estén funcionando
echo -e "\n${BLUE}🔍 Verificando estado de los servicios...${NC}"
docker service ls --filter name="${STACK_NAME}"

# Mostrar información para acceder a los servicios
MANAGER_IP=$(docker node inspect self --format '{{ .Status.Addr }}')
echo -e "\n${GREEN}✨ Despliegue completado. Accede a los servicios:${NC}"
echo -e "- API Gateway: http://${MANAGER_IP}:5000"
echo -e "- Cliente Web: http://${MANAGER_IP}:8080"
echo -e "- RabbitMQ Admin: http://${MANAGER_IP}:15672 (usuario: admin, contraseña: adminpass)"