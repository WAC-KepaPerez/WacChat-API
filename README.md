# WacChatAPI

## Descripción
Este proyecto es una aplicación Django Rest Framework para el plugin WacChat-Plugin.

## Instalación
1. Clona el repositorio:
    ```bash
    git clone https://github.com/WAC-KepaPerez/WacChat-API
    ```
2. Navega hasta el directorio del proyecto:
    ```bash
    cd WacChat-API
    ```
3. Instala las dependencias usando pip:
    ```bash
    pip install -r requirements.txt
    ```

## Uso
1. Crea un archivo `.env` en el directorio raíz del proyecto.
2. Define las variables de entorno en el archivo `.env`. Por ejemplo:
    ```plaintext
        OPENAI_API_KEY="tu clave de API"
        PINECODE_API_KEY="tu clave de API"
    ```
3. Ejecuta migraciones (no necesario):
    ```bash
    python manage.py migrate
    ```
4. Inicia el servidor de desarrollo:
    ```bash
    python manage.py runserver
    ```

## Licencia
[Inserta la licencia de tu proyecto aquí.]
