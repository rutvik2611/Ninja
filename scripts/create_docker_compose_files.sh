#!/bin/bash

# Create the script directory if it doesn't exist
mkdir -p script

# Create the docker-compose-db.yml file
cat << EOF > script/docker-compose-db.yml
version: '3.1'

services:
    db:
        image: postgres
        restart: always
        environment:
            POSTGRES_PASSWORD: example
        volumes:
            - postgres_data:/var/lib/postgresql/data/

volumes:
    postgres_data:

networks:
    default:
        external: true
        name: my_network
EOF

# Create the docker-compose-pgadmin.yml file
cat << EOF > script/docker-compose-pgadmin.yml
version: '3.1'

services:
    pgadmin:
        image: dpage/pgadmin4
        restart: always
        environment:
            PGADMIN_DEFAULT_EMAIL: user@example.com
            PGADMIN_DEFAULT_PASSWORD: secret
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.pgadmin.rule=Host('localhost')"
            - "traefik.http.services.pgadmin.loadbalancer.server.port=80"
        depends_on:
            - db

networks:
    default:
        external: true
        name: my_network
EOF

# Create the docker-compose-traefik.yml file
cat << EOF > script/docker-compose-traefik.yml
version: '3.1'

services:
    traefik:
        image: traefik:v2.0
        command:
            - "--api.insecure=true"
            - "--providers.docker=true"
            - "--providers.docker.exposedbydefault=false"
            - "--entrypoints.web.address=:80"
        ports:
            - "80:80"
            - "8080:8080"
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock

networks:
    default:
        external: true
        name: my_network
EOF

echo "Docker Compose files have been created in the script directory."