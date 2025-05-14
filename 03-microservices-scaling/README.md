## ST0263 Tópic. Espec. en Telemática - Proyecto 2

### Integrantes

- Alejandro Ríos Muñoz - ariosm@eafit.edu.co
- Lina Sofía Ballesteros Merchán - lsballestm@eafit.edu.co
- Jhonnatan Stiven Ocampo Díaz - jsocampod@eafit.edu.co

### Profesor

- Edwin Nelson Montoya Munera - emontoya@eafit.edu.co

### 1. Descripción del proyecto

Este proyecto implementa una arquitectura de microservicios escalables utilizando Flask y RabbitMQ para la mensajería asíncrona. Cada microservicio está encargado de un dominio específico: Autenticación, Catálogo de Libros y Gestión de Órdenes. Los microservicios se comunican a través de una API Gateway que actúa como un punto único de acceso para el cliente. Además, la comunicación entre microservicios incluye eventos en tiempo real.

### 2. Información general

#### 2.1 Diseño de alto nivel
El sistema está compuesto por los siguientes componentes:
- API Gateway (Flask): Actúa como el punto único de entrada para todas las solicitudes del cliente, autentica las solicitudes y las redirige a los microservicios correspondientes.
- Microservicio de Autenticación: Gestiona el registro, login y la generación de tokens JWT para la autenticación de usuarios.
- Microservicio de Catálogo: Gestiona la información de los libros, incluidos su creación, modificación y eliminación.
- Microservicio de Órdenes: Gestiona las órdenes de compra de los usuarios, incluyendo la creación de órdenes y el procesamiento de pagos.
- RabbitMQ: Utilizado para la gestión de eventos entre los microservicios (creación, actualización y eliminación de libros).
- Base de datos (MySQL): Cada microservicio tiene su propia base de datos para almacenar los datos de usuarios, libros y órdenes.

![image](https://github.com/user-attachments/assets/d73e75e8-7b3f-4826-9dd8-686a508fe973)

#### 2.2 Arquitectura
El sistema utiliza la arquitectura de microservicios y se gestiona con Docker Swarm para escalar los microservicios de forma horizontal.

#### 2.3 Patrones de diseño
- Microservicios: Cada servicio es independiente y realiza una función específica.
- API Gateway: Se utiliza para centralizar las solicitudes y gestionar la autenticación.
- Event-Driven: Los eventos relacionados con los libros son gestionados a través de RabbitMQ, lo que permite una comunicación asíncrona entre los servicios.

#### 2.4 Buenas prácticas utilizadas
- Modularización del código
- Uso de patrones de diseño como microservicios y eventos.
- Escalabilidad horizontal con Docker Swarm.

### 3. Descripción del ambiente de desarrollo y técnico
#### 3.1 Lenguajes y tecnologías principales

| Componente           | Tecnología         | Versión               |
|----------------------|--------------------|------------------------|
| Frontend             | Flask (Python)     | 3.1.0                 |
| API Gateway          | Flask (Python)     | 3.1.0                 |
| Microservicios       | Flask (Python)     | 3.1.0                 |
| Bases de datos       | MariaDB            | 10.4.32               |
| Middleware (MOM)     | RabbitMQ           | 4.x (Management UI)   |
| Orquestación         | Docker Swarm       | Docker 24.0.5         |
| Contenedores         | Docker Engine      | 24.0.5                |

#### 3.2 Detalles del desarrollo
Este proyecto utiliza el patrón de microservicios para cada funcionalidad del sistema. Además, cada microservicio tiene su propia base de datos.

#### 3.3 Estructura del proyecto
```bash
.
├── api-gateway/                 # API Gateway (Flask)
├── client/                       # Cliente (Frontend en Flask)
├── microservices/
│   ├── auth-service/             # Microservicio de Autenticación
│   ├── catalog-service/          # Microservicio de Catálogo
│   └── order-service/            # Microservicio de Órdenes
├── docker-compose.yml           # Archivo para levantar todos los servicios
└── README.md                    # Documentación del proyecto

```
### 4. Despliegue del Proyecto en Docker Swarm
Para poner en marcha el clúster Docker Swarm y desplegar los microservicios, sigue estos pasos detallados:

#### 4.1 Configuración de la infraestructura
1. Crear un Security Group en la consola de AWS con los siguientes puertos abiertos:

* TCP - 2377
* TCP - 7946
* UDP - 7946
* UDP - 4789
* TCP - 5000-5003
* TCP - 8080
* TCP - 5672
* TCP - 15672
* MYSQL/AURORA - 3306

2. Crear 3 instancias EC2 con características **t2.medium** y **16 GiB gp3**, asignándolas al mismo grupo de seguridad.

#### 4.2 Instalación de dependencias
En cada instancia, instala las dependencias necesarias:
```bash
sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y

sudo systemctl enable docker
sudo systemctl start docker
```

#### 4.3 Configurar permisos para Docker
Haz que el usuario ubuntu tenga permisos para ejecutar Docker sin necesidad de usar sudo:

```bash
sudo usermod -a -G docker ubuntu
```

Recuerda refrescar la página de la instancia para aplicar los cambios.

#### 4.4 Inicializar Docker Swarm en el nodo manager
1. En el nodo manager, inicializa Docker Swarm con el siguiente comando:

```bash
sudo docker swarm init
```
2. Luego, obtén el token para unir los nodos worker al clúster:

```bash
sudo docker swarm join-token manager
```

#### 4.5 Unir nodos worker al clúster
En cada nodo worker, ejecuta el token generado para unirte al clúster:

```bash
sudo docker swarm join --token <token>
```

#### 4.6 Desplegar la aplicación usando Docker Swarm
1. En el nodo manager, clona el repositorio y navega al directorio del proyecto:

```bash
git clone https://github.com/alejoriosm04/bookstore-ecommerce.git
cd bookstore-ecommerce/03-microservices-scaling/
```
2. Concede permisos de ejecución al archivo de despliegue:
```bash
chmod +x swarm-deploy.sh
```
3. Ejecuta el script de despliegue:

```bash
sudo -E ./swarm-deploy.sh
```

**Durante el despliegue, si ves errores de tipo "Task failure", presiona CTRL+C y vuelve a ejecutar el script varias veces hasta que los servicios se levanten correctamente.**

### Referencias
Docker. (n.d.). Swarm mode overview. Docker. Recuperado el 13 de mayo de 2025, de https://docs.docker.com/engine/swarm/

Flask. (n.d.). Flask documentation. Flask. Recuperado el 13 de mayo de 2025, de https://flask.palletsprojects.com/en/stable/
