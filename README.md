# Paginho - TPE BD2

## Requisitos
- `Docker`
- `Python >= 3.10` 
<p>&nbsp;</p>

## Instalación de Bases de Datos

Para instalar las bases de datos necesarias para la ejecución de la API debemos ejecutar el script `setup_db.sh`, este genera cuatro contenedores en Docker que levantan y crean las bases de datos corrrespondientes.
```sh
chmod +x setup_db.sh
./setup_db.sh
```
<p>&nbsp;</p>

## Instalación de dependencias de Python
```sh
chmod +x dependency-script.sh
./dependency-script.sh
```
<p>&nbsp;</p>

## Ejecución

### Ejecución Paginho API

Una vez corriendo las bases de datos necesarias, en este caso redis (`:6379`) y postgres (`:5432`) en los puertos indicados.
Para ejectuar la API de Paginho ejecutamos el siguiente comando:

```sh
cd paginho
uvicorn main:app --reload --port 8000
```

Para acceder a la documentación de swagger, ir a `http://localhost:8000/docs` en el navegador. <br/>
En caso de querer modificar los parámetros de la base de datos, puede hacerse desde el archivo `.env`

<p>&nbsp;</p>

### Ejecución Financial Entity SQL API

Una vez corriendo la base de datos postgres (`:5433`) en el puerto indicado.
Para ejectuar la API de entidad financiera que utiliza un Postgres como mecanismo de persistencia ejecutamos el siguiente comando:

```sh
cd financialEntitySql
uvicorn main:app --reload --port 8001
```

Para acceder a la documentación de swagger, ir a `http://localhost:8001/docs` en el navegador. <br/>
En caso de querer modificar los parámetros de la base de datos, puede hacerse desde el archivo `.env`

<p>&nbsp;</p>

### Ejecución Financial Entity Mongo API

Una vez corriendo la base de datos mongo (`:27017`) en el puerto indicado.
Para ejectuar la API de entidad financiera que utiliza un MongoDb como mecanismo de persistencia ejecutamos el siguiente comando:

```sh
cd financialEntityMongo
uvicorn main:app --reload --port 8002
```

Para acceder a la documentación de swagger, ir a `http://localhost:8002/docs` en el navegador. <br/>
En caso de querer modificar los parámetros de la base de datos, puede hacerse desde el archivo `.env`

<p>&nbsp;</p>

## Autores

- 60460 - Larroudé Alvarez, Santiago Andrés
- 61361 - Mattiussi, Agustín Hernán
- 61535 - Sasso, Julían Martín

## Documentación Adicional

[Trabajo Práctico Final BD2 - 2023 1C (Paginho), Notion.so](https://www.notion.so/Trabajo-Pr-ctico-Final-BD2-2023-1C-Paginho-98b3855562a8427db6a494828b7c9422)