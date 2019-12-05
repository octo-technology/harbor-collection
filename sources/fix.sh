#!/bin/bash

helm upgrade airflow bitnami/airflow \
    --set service.type=LoadBalancer,airflow.baseUrl=http://$APP_HOST:$APP_PORT,airflow.auth.password=$APP_PASSWORD,postgresql.postgresqlPassword=$APP_DATABASE_PASSWORD,redis.password=$APP_REDIS_PASSWORD
