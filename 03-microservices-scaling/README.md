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

#### 3.2 Cómo compilar y ejecutar el proyecto

Clonar el repositorio en el equipo local.
```bash
git clone https://github.com/alejoriosm04/rpc-mom-comm.git
```

Configurar las variables de entorno. Cada microservicio requiere variables de entorno para la configuración de la base de datos y RabbitMQ.
```bash
cp .env.example .env
```

Crear las bases de datos, Para cada microservicio, ejecutar lo siguiente para crear las tablas en las bases de datos respectivas:
```bash
flask shell
>>> from app.models import db
>>> db.create_all()
```

#### 3.3 Detalles del desarrollo
Este proyecto utiliza el patrón de microservicios para cada funcionalidad del sistema. Además, cada microservicio tiene su propia base de datos.

#### 3.4 Estructura del proyecto
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

### Referencias
Docker. (n.d.). Swarm mode overview. Docker. Recuperado el 13 de mayo de 2025, de https://docs.docker.com/engine/swarm/

Flask. (n.d.). Flask documentation. Flask. Recuperado el 13 de mayo de 2025, de https://flask.palletsprojects.com/en/stable/
