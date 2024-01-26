# Script de Gestión de radippool para FreeRADIUS

Este script de Python está diseñado para ayudar a gestionar y mantener los bloques IPv4 en la tabla `radippool` de FreeRADIUS, con cada bloque asignado a un nombre de pool específico. Automatiza el proceso de asegurar que todos los bloques IPv4 y nombres de pools especificados en un archivo de configuración YAML estén presentes en la tabla `radippool`, insertando cualquier dirección IP y pool faltante.

## Requisitos Previos

Antes de utilizar este script, asegúrate de tener lo siguiente:

* Python 3.x instalado en tu sistema.
* Acceso a una base de datos MySQL que contenga la tabla `radippool` de FreeRADIUS.
* Los paquetes PyMySQL y PyYAML instalados en tu entorno Python.

## Instalación

Para utilizar este script, primero clona el repositorio o descarga los archivos directamente. Luego, instala las dependencias necesarias:

```bash
git clone https://github.com/aweher/python-radippool.git
cd python-radipool
python3 -m venv .venv
source .venv/bin/activate
pip3 install PyMySQL PyYAML
cp config.yaml.example config.yaml
```

## Archivo de Configuración

El script lee la configuración de un archivo `config.yaml` que debe estar en el mismo directorio que el script. Este archivo debe contener los parámetros de conexión a la base de datos y los bloques IPv4 con sus nombres de pools correspondientes. También se le pueden especificar IPs a exceptuar de forma individual. Aquí tienes un ejemplo de este archivo:

```yaml
database:
  host: "localhost"
  user: "usuario_db"
  password: "contraseña_db"
  db_name: "nombre_db"

ipv4_pools:
  - pool_name: "Pool1"
    block: "192.168.1.0/24"
    exceptions:
    - "192.168.1.88"
    - "192.168.1.1"
  - pool_name: "Pool2"
    block: "192.168.2.0/24"
  # Agrega más bloques y nombres de pools según sea necesario
```

## Ejecución

Para ejecutar el script, entra al directorio que contiene `app.py` y `config.yaml`, y luego ejecuta:

```bash
python3 app.py
```

El script leerá el archivo de configuración, se conectará a la base de datos MySQL especificada y asegurará que todos los bloques IPv4 listados estén presentes en la tabla radippool, insertando cualquier dirección IP faltante con el nombre de Pool correspondiente.

## Contribuciones

Las contribuciones a este proyecto son bienvenidas. Para contribuir, por favor, haz un fork del repositorio, realiza tus cambios y envía un pull request.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE para obtener más detalles.
