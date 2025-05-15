# Tópicos especiales en Telemática ST0263 2025-1 - Proyecto 2 - Escalamiento y despliegue distribuido de app Bookstore

### Estudiantes:

* Juan Diego Llorente Ortega
  * jdllorento@eafit.edu.co
* Santiago Gómez Rueda
  * sgomezr13@eafit.edu.co
* Samuel Daza Carvajal
  * sdazac@eafit.edu.co
 
### Profesor
* Edwin Nelson Montoya
  * emontoya@eafit.brightspace.com
 
## 1. Breve descripción de la actividad
El objetivo de esta actividad fue escalar y desplegar en diferentes escenarios en la nube (AWS) una aplicación monolítica de venta de libros, implementada con Flask y MySQL. La arquitectura migró desde una versión local a una estructura distribuida utilizando servicios gestionados y patrones de escalabilidad, incluyendo autoescalamiento, balanceo de carga, almacenamiento compartido, y base de datos administrada.

### 1.1 ¿Qué aspectos se cumplieron?
Para el objetivo 1:

- Despliegue en una única instancia EC2.
- Uso de nombre de dominio propio.
- Certificado SSL para tráfico HTTPS.
- Proxy inverso con NGINX.

Para el objetivo 2:

- Despliegue en máquinas virtuales EC2 a través de un Auto Scaling Group (ASG).
- Balanceo de carga con Application Load Balancer (ALB).
- Redirección HTTP a HTTPS mediante certificado SSL de ACM (Amazon Certificate Manager).
- Uso de imagen Docker personalizada y ejecutada vía `docker-compose`.
- Base de datos administrada con Amazon RDS (MySQL), configurada como Multi-AZ.
- Almacenamiento compartido entre instancias usando Amazon EFS.
- Uso de Elastic IP, dominio propio (kreadesig.com) y configuración DNS con Route 53.
- Automatización del arranque con script `start.sh` incluido en una AMI personalizada.
- Acceso completo por dominio personalizado usando `https://kreadesig.com` y `https://www.kreadesig.com`.

Para el objetivo 3:

- Se creo una instancia EC2 en la cual se incio un docker swarm
- La docker image actual se subio a dockerhub
- Se inciaron 5 contenedores en el swarm con la imagen del proyecto
- Se creo otro grupo de destino para que el load balancer apunte al docker swarm tambien
- Es posible aumentar las instancias y el numero de contenedores facilmente

## 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas

- Arquitectura monolítica desacoplada mediante contenedores Docker.
- Escalamiento horizontal mediante Auto Scaling.
- Balanceo de carga usando ALB.
- Separación de preocupaciones: app, base de datos, almacenamiento.
- Tolerancia a fallos con Multi-AZ en RDS y replicación automática.
- Persistencia compartida con EFS montado como volumen en contenedores.
- Seguridad HTTPS centralizada en ALB con ACM.
- Scripts de arranque (`start.sh`) para garantizar consistencia al iniciar instancias.

## 3. Descripción del ambiente de desarrollo y técnico

- Lenguaje principal: Python 3.10
- Framework web: Flask
- Base de datos: MySQL 8
- Contenerización: Docker + Docker Compose
- Sistema operativo: Ubuntu 22.04 LTS en EC2
- Control de versiones: Git, Docker Hub
- Infraestructura: AWS (EC2, ALB, RDS, EFS, Route 53)

### Paquetes y requerimientos

- flask
- flask_sqlalchemy
- flask_login
- pymysql
- werkzeug

### Detalles técnicos

- El contenedor de la aplicación recibe la URI de conexión a RDS mediante variable de entorno SQLALCHEMY_DATABASE_URI.
- El volumen compartido /mnt/bookstore se monta dentro del contenedor en /app/shared.
- Se utiliza un Dockerfile para construir la imagen con python:3.10-slim.

### Configuración del proyecto

- DATABASE_URL: conexión a RDS (mysql+pymysql://user:password@host:port/db)
- Volumen compartido: /mnt/bookstore:/app/shared
- Puerto expuesto: 5000

### Cómo ejecutar

En general, solo habría que poner a correr el contenedor:

```
docker-compose up -d
```

Para el escenario 1, donde es una sola instancia corriendo el proyecto, el contenedor se inicia automáticamente con la instancia, solo hay que acceder a la dirección: legacy.kreadesig.com, este registro está asociado únicamente a la instancia de despliegue monolítico con NGINX

Para el escenario 2, solo hay que acceder a el nombre de dominio (kreadesig.com o www.kreadesig.com) y en caso de ser a través de HTTP se redirige a HTTPS

### Parámetros configurables

- Se podrían cambiar los registros DNS a través de Route 53 de AWS entrando a la zona alojada kreadesig.com
- El string de conexión a la base de datos, se cambia en config.py y es utilizado en app.py
- En cuanto a puertos no es recomendable cambiar nada en grupos de seguridad, ya que se usan puertos bien conocidos y estandarizados para los servicios usados

### Capturas del funcionamiento
![image](https://github.com/user-attachments/assets/29e903d8-8a77-4d3a-8d16-08785ca775e8)

Acceso HTTPS a la aplicación desplegada
![image](https://github.com/user-attachments/assets/8d65e96b-d472-4618-9c0f-3f76e36474eb)

Despliegue con Docker
![image](https://github.com/user-attachments/assets/9047f518-926c-4809-9433-5621775c292a)

Acceso HTTPS a la aplicación monolítica desplegada
![image](https://github.com/user-attachments/assets/9581ce83-efee-4236-b887-99d65f374b14)
![image](https://github.com/user-attachments/assets/200d28d0-dd78-43b4-aece-d483dfdeca51)

NFS montado en las instancias y archivos que han sido compartidos


## 4. Ambiente de ejecución (producción)

### Infraestructura en AWS

- EC2 con AMI personalizada (contenedor y montaje preconfigurado)
- Auto Scaling Group con instancias en múltiples AZ
- Load Balancer con listeners en puertos 80 y 443
- Base de datos en Amazon RDS Multi-AZ (MySQL)
- Almacenamiento en red con Amazon EFS
- DNS gestionado por Route 53
- Dominio: https://kreadesig.com

### Parámetros y configuración en producción

- Certificado SSL en ACM (Amazon Certificate Manager) para kreadesig.com y www.kreadesig.com
- start.sh incluido en la AMI y ejecutado al arranque desde User Data
- Rutas de salud definidas en ALB (/) con puerto 5000
- Redirección automática de HTTP a HTTPS

### ¿Cómo se lanza el servidor?

- El Auto Scaling Group crea instancias basadas en la AMI
- Al arrancar, ejecutan /home/ubuntu/bookstore/start.sh
- Este script monta EFS, hace docker pull y levanta la app con docker-compose

### Mini guía de uso de la app

- Ingresar al dominio: https://kreadesig.com
- Registrarse como usuario
- Iniciar sesión
- Agregar libros, realizar compras, visualizar información

## 5. Otra información relevante

- La infraestructura es tolerante a fallos a nivel de aplicación y base de datos (usando Multi-AZ)
- Se puede escalar automáticamente según demanda gracias al ASG manteniendo el uso de CPU en máximo 60% con máximo 3 instancias creadas.
- El almacenamiento persistente entre instancias facilita futuras extensiones (como subida de archivos).
- La AMI puede ser actualizada fácilmente con una nueva imagen dockerizada para desplegar nuevas versiones.

# Referencias

- Código fuente de la aplicación: https://github.com/st0263eafit/st0263-251/blob/main/proyecto2/BookStore.zip
- https://docs.aws.amazon.com/efs
- https://docs.aws.amazon.com/elasticloadbalancing
- https://hub.docker.com

# Enlaces de versiones

- Este repo: https://github.com/jdllorento/bookstore-deployment/tree/main
- Imagen de Docker: https://hub.docker.com/repository/docker/jdllorento/bookstore-app/general
