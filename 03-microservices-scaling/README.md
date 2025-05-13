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
| Componente           | Tecnología         | Versión               |
|----------------------|--------------------|------------------------|
| Frontend             | Flask (Python)     | 3.1.0                 |
| API Gateway          | Flask (Python)     | 3.1.0                 |
| Microservicios       | Flask (Python)     | 3.1.0                 |
| Bases de datos       | MariaDB            | 10.4.32               |
| Middleware (MOM)     | RabbitMQ           | 4.x (Management UI)   |
| Orquestación         | Docker Swarm       | Docker 24.0.5         |
| Contenedores         | Docker Engine      | 24.0.5                |







