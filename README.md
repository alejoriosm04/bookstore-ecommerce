# ST0263 Tópicos Especiales en Telemática - Proyecto 2

## Integrantes

* Alejandro Ríos Muñoz - [ariosm@eafit.edu.co](mailto:ariosm@eafit.edu.co)
* Lina Sofía Ballesteros Merchán - [lsballestm@eafit.edu.co](mailto:lsballestm@eafit.edu.co)
* Jhonnatan Stiven Ocampo Díaz - [jsocampod@eafit.edu.co](mailto:jsocampod@eafit.edu.co)

## Profesor

* Edwin Nelson Montoya Munera - [emontoya@eafit.edu.co](mailto:emontoya@eafit.edu.co)

---

# Índice

1. Descripción del proyecto
   1.1 Requerimientos funcionales y no funcionales
   1.2 Aspectos no desarrollados
2. Información general
   2.1 Diseño de alto nivel
   2.2 Arquitectura
   2.3 Patrones de diseño
   2.4 Buenas prácticas utilizadas
3. Ambiente de desarrollo y técnico
   3.1 Lenguajes y tecnologías principales
   3.2 Compilación y ejecución
   3.3 Detalles del desarrollo
   3.4 Estructura del proyecto
   3.5 Descripción de los componentes
4. Ambiente de ejecución (Producción)
   4.1 Despliegue
   4.2 IP o nombre de dominio del servidor
   4.3 Mini guía para el usuario final
5. Referencias

---

## 1. Descripción del proyecto

BookStore es una aplicación web de comercio electrónico para la venta de libros de segunda mano, publicada por usuarios registrados. Soporta autenticación, visualización de catálogo, compra, pago y envío simulado.

El proyecto se desarrolló en tres etapas progresivas:

* **Objetivo 1:** Despliegue monolítico en una sola instancia EC2 con Docker, NGINX y Certbot para SSL.
* **Objetivo 2:** Escalamiento horizontal con Auto Scaling Group, RDS, EFS y certificados SSL gestionados con ACM.
* **Objetivo 3:** Reingeniería completa de la aplicación en una arquitectura de microservicios desplegada con Docker Swarm y RabbitMQ.

### 1.1 Requerimientos funcionales y no funcionales

#### Funcionales

* RF01: Registro, login y logout de usuarios
* RF02: Visualización de catálogo de libros
* RF03: Compra de libros (simulada)
* RF04: Pago y envío simulado
* RF05: Separación de funcionalidades en microservicios (objetivo 3)

#### No funcionales

* RNF01: Certificado SSL para el acceso por HTTPS
* RNF02: Balanceo de carga y alta disponibilidad (objetivo 2 y 3)
* RNF03: Contenerización y despliegue reproducible con Docker

### 1.2 Aspectos NO desarrollados

* No se usó Kubernetes (EKS) por restricciones de la cuenta AWS Academy
* La interfaz de usuario fue simulada o mantenida con una versión web sencilla (en vez de Next.js)

---

## 2. Información general

### 2.1 Diseño de alto nivel

* Monolito: NGINX como proxy inverso hacia una app Flask, con MySQL y Docker Compose
* Escalado: Arquitectura tradicional de 3 capas con Auto Scaling, RDS y EFS
* Microservicios: Gateway en FastAPI y microservicios desacoplados con sus propias bases de datos

### 2.2 Arquitectura

* Objetivo 1: Monolítico con NGINX, Flask, MySQL, Docker Compose, certificado SSL y dominio
* Objetivo 2: Auto Scaling Group (EC2), ELB, RDS, EFS y certificado SSL gestionado por ACM
* Objetivo 3: Microservicios con Docker Swarm, RabbitMQ, API Gateway y gRPC

### 2.3 Patrones de diseño

* Microservicios por dominio funcional
* API Gateway como punto de entrada centralizado
* Separación de responsabilidades (auth, catalog, orders)
* CQRS aplicado en ordenes y catálogo para actualización sincronizada

### 2.4 Buenas prácticas utilizadas

* Contenerización con Docker y Docker Compose
* Uso de redes internas y secretos para seguridad
* Uso de .env para configuración sensible
* Orquestación con Docker Swarm para microservicios

---

## 3. Ambiente de desarrollo y técnico

### 3.1 Lenguajes y tecnologías principales

| Componente         | Tecnología      | Versión    |
| ------------------ | --------------- | ---------- |
| Backend Monolito   | Python + Flask  | 3.9 / 3.1  |
| Base de datos      | MySQL / MariaDB | 8.0 / 10.4 |
| Web Server         | NGINX           | 1.25.3     |
| Certificados SSL   | Certbot / ACM   | Latest     |
| Orquestación       | Docker / Swarm  | 24.0.5     |
| Mensajería (obj 3) | RabbitMQ        | 4.x        |
| Gateway (obj 3)    | FastAPI         | 0.110.0    |

### 3.2 Compilación y ejecución

* `docker-compose up -d` para levantar el monolito (objetivo 1)
* Auto Scaling y Launch Template para levantar instancias EC2 (objetivo 2)
* `docker swarm init && docker stack deploy` para microservicios (objetivo 3)

### 3.3 Detalles del desarrollo

* La app Flask usa Blueprints, SQLAlchemy, y Jinja2
* Scripts para iniciar servicios en segundo plano en instancias EC2
* Configuración persistente de volúmenes Docker y secretos

### 3.4 Estructura del proyecto

```
bookstore-ecommerce/
├── 01-monolithic/
│   ├── controllers/
│   ├── models/
│   ├── templates/
│   ├── app.py
│   └── docker-compose.yml
├── 02-monolithic-scaling/
│   ├── launch-template.sh
│   ├── terraform/
│   └── efs-mount/
└── 03-microservices-scaling/
    ├── api-gateway/
    ├── microservices/
    │   ├── auth-service/
    │   ├── catalog-service/
    │   └── order-service/
    └── docker-compose.yml
```

### 3.5 Descripción de los componentes

* **Monolito:** Flask App modularizada, base de datos local MySQL
* **Escalado:** Misma imagen desplegada en EC2 autoescalables con volúmenes compartidos EFS y base de datos externa RDS
* **Microservicios:** Auth, Catalog, Orders con RabbitMQ y API Gateway en FastAPI usando gRPC y CQRS

---

## 4. Ambiente de ejecución

### Objetivo 1

* Desplegado en EC2 con Docker Compose
* Dominio personalizado con NO-IP y certificado SSL generado con Certbot
* Flask y MySQL como contenedores

### Objetivo 2

* Auto Scaling Group con AMI personalizada
* ELB como balanceador de carga
* RDS Aurora como base de datos administrada
* EFS como sistema de archivos compartido
* Certificado SSL gestionado con ACM

### Objetivo 3

* Despliegue distribuido con Docker Swarm
* API Gateway FastAPI + gRPC
* RabbitMQ para mensajes asincrónicos
* Cada microservicio con su propia base de datos

### 4.3 Mini guía para el usuario final

1. Registro y autenticación de usuarios
2. Exploración del catálogo de libros
3. Agregar libros al carrito y realizar compras
4. Verificación de stock y proceso de pago simulado

---

## 5. Referencias

* [AWS Documentation](https://docs.aws.amazon.com/)
* [Docker Documentation](https://docs.docker.com/)
* [Flask Microservices](https://flask.palletsprojects.com/)
* [RabbitMQ Docs](https://www.rabbitmq.com/documentation.html)
* [Certbot](https://certbot.eff.org/)
* Repositorio base: [https://github.com/st0263eafit/st0263-251/blob/main/proyecto2/BookStore.zip](https://github.com/st0263eafit/st0263-251/blob/main/proyecto2/BookStore.zip)
