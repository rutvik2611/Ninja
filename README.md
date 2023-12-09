# Ninja

## Overview

Ninja is a Python-based application that uses Docker for containerization. The application is set up with a variety of services, each with its own Docker Compose file. The services are orchestrated using these Docker Compose files.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository.
2. Navigate to the project directory in your terminal.

## Running the Project

1. Ensure Docker and Docker Compose are installed on your machine. You can check this by running `docker --version` and `docker-compose --version` in your terminal. If these commands return a version number, Docker and Docker Compose are installed. If not, you will need to install them.

2. Run the `run.sh` script to start the application. If the script is not executable, you may need to make it executable by running `chmod +x run.sh`.

```bash
./run.sh