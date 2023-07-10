#!/bin/bash

# Borrar contenedores de Redis, PostgreSQL y MongoDB y todos los datos
docker-compose down -v

# Iniciar contenedores de Redis, PostgreSQL y MongoDB
docker-compose up -d
# Redis container name: redis_container
# PostgreSQL container name: postgres_container_paginho
# PostgreSQL container name: postgres_container_financialEntity
# MongoDB container name: mongo_container

# Esperar a que los contenedores de Redis, PostgreSQL y MongoDB estén en línea
while ! docker exec -t redis_container redis-cli PING > /dev/null 2>&1; do
  sleep 1
done

while ! docker exec -t postgres_container_paginho pg_isready -U postgres -d postgres -h localhost > /dev/null 2>&1; do
  sleep 1
done

while ! docker exec -t postgres_container_financialEntity pg_isready -U postgres -d postgres -h localhost > /dev/null 2>&1; do
  sleep 1
done

while ! docker exec -t mongo_container mongo --eval "db.stats()" > /dev/null 2>&1; do
  sleep 1
done

# docker cp schema_redis_data.txt redis_container:schema_redis_data.txt
# docker cp schemaPostgres.sql postgres_container:schemaPostgres.sql
# docker cp financialEntity.sql postgres_container:financialEntity.sql
# docker cp schema_mongodb_data.js mongo_container:schema_mongodb_data.js

# Cargar datos en Redis
# docker exec -i redis_container redis-cli < schema_redis_data.txt

# Cargar datos en PostgreSQL
# docker exec -i postgres_container_paginho psql -U postgres -d postgres -f schemaPostgres.sql
# docker exec -i postgres_container_financialEntity psql -U postgres -d postgres -f financialEntity.sql

# Cargar datos en MongoDB
# docker exec -i mongo_container mongo < schema_mongodb_data.js
