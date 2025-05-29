# ORM SQLAlchemy

## Docker / PostgreSQL

### Start the project

```bash
docker-compose up -d # runs in background
docker-compose logs -f # view logs after launch
docker-compose up # runs and shows logs
```

### Stop the project

```bash
docker-compose down
```

### Restart the project (preserving data)

```bash
docker-compose restart
```

---

## Alembic (Migrations)

### Initialize Alembic (once)

```bash
alembic init migrations
```

### Configuration

- In `alembic.ini`, set the correct `SQLALCHEMY_DATABASE_URL`
- In `migrations/env.py`, import `Base` from your models:

```python
from your_project.models import Base
```

### Create a migration

```bash
alembic revision --autogenerate -m "Initial migration"
```

### Apply migration

```bash
alembic upgrade head
```

---

## ✅ Useful Commands

### Check current migration status

```bash
alembic current
```

### Check Docker container logs

```bash
docker logs <container_name>
```

### Access Postgres container

```bash
docker exec -it some-postgres psql -U postgres
```

---

> Note: Make sure the PostgreSQL Docker container has a properly configured volume if you want to persist data between restarts.
