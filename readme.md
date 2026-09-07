This project demonstrates UI, API, database, and hybrid test automation.

# OrangeHRM Pytest Automation Framework

## Running OrangeHRM with Docker

The project uses a local Docker-based OrangeHRM environment for UI, API, and database testing.

### Starting OrangeHRM after a system restart

After restarting the laptop, Docker Desktop must be running before starting the OrangeHRM containers.

Check the container status:

docker compose -f docker-orangehrm\docker-compose.yml ps

If the containers are not running, start them in detached mode:

docker compose -f docker-orangehrm\docker-compose.yml up -d

Verify that both containers are running:

docker compose -f docker-orangehrm\docker-compose.yml ps

Expected services:

- orangehrm → available at http://localhost:8080
- mariadb → available at localhost:3306

### Docker data persistence

The MariaDB database uses a Docker named volume to persist data.

Restarting the laptop or stopping the containers does not delete the OrangeHRM database.

To stop the containers:

docker compose -f docker-orangehrm\docker-compose.yml down

The database volume is preserved.

To stop the containers and delete the database volume:

docker compose -f docker-orangehrm\docker-compose.yml down -v

> docker compose down -v deletes the MariaDB volume and resets the OrangeHRM database. Use it only when a fresh database installation is required.

### Docker Compose configuration

The Docker environment is defined in:

docker-orangehrm/docker-compose.yml

The Compose setup contains:

- OrangeHRM 5.9 application container
- MariaDB 11 database container
- Persistent MariaDB Docker volume
- OrangeHRM exposed on port 8080
- MariaDB exposed on port 3306

### Environment configuration

Docker database credentials are stored in the project's .env file and are not committed to Git.

The application and test framework also use environment-specific configuration through .env.

The current local QA environment uses the Docker-based OrangeHRM instance:

QA_ORANGEHRM_BASE_URL=http://localhost:8080

### Useful Docker commands

Check running containers:

docker compose -f docker-orangehrm\docker-compose.yml ps

Start containers:

docker compose -f docker-orangehrm\docker-compose.yml up -d

View all container logs:

docker compose -f docker-orangehrm\docker-compose.yml logs

View OrangeHRM logs:

docker compose -f docker-orangehrm\docker-compose.yml logs orangehrm

View MariaDB logs:

docker compose -f docker-orangehrm\docker-compose.yml logs mariadb

Stop containers:

docker compose -f docker-orangehrm\docker-compose.yml down

Stop containers and remove the database volume:

docker compose -f docker-orangehrm\docker-compose.yml down -v

### Running the test suite

Make sure Docker Desktop is running and both OrangeHRM and MariaDB containers are up before running tests.

Run the complete test suite:

pytest -v

Run tests in parallel:

pytest -n 4 -v

Run tests against a specific environment:

pytest -v --env qa