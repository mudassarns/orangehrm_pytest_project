## Running OrangeHRM with Docker

The project uses a local Docker-based OrangeHRM environment for UI, API, and database testing.

### Starting OrangeHRM after a system restart

After restarting the laptop, Docker Desktop must be running before starting the OrangeHRM containers.

Check the container status:

```powershell
docker compose -f docker-orangehrm\docker-compose.yml ps

If the containers are not running, start them in detached mode:

docker compose -f docker-orangehrm\docker-compose.yml up -d

Verify that both containers are running:

docker compose -f docker-orangehrm\docker-compose.yml ps

Expected services:

orangehrm → available at http://localhost:8080
mariadb → available at localhost:3306