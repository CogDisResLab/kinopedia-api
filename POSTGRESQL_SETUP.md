\# PostgreSQL Setup Guide



\## Installation



\### Windows:

Download from: https://www.postgresql.org/download/windows/

Follow installer instructions.



\## Database Setup



Open Command Prompt:



```cmd

\# Create database

createdb kinopedia



\# Create user

psql -U postgres

CREATE USER kinopedia\_user WITH PASSWORD 'your\_password';

GRANT ALL PRIVILEGES ON DATABASE kinopedia TO kinopedia\_user;

\\q

```



\## Migration from SQLite



Install migration dependencies:

```cmd

pip install asyncpg

```



Update `app/database.py`:



```python

DATABASE\_URL = "postgresql+asyncpg://kinopedia\_user:password@localhost/kinopedia"

```



\## Connection String Format



postgresql+asyncpg://username:password@host:port/database



Example:

postgresql+asyncpg://kinopedia\_user:mypassword@localhost:5432/kinopedia



\## Notes



\- For this phase, SQLite is sufficient

\- PostgreSQL setup is for future production deployment

\- All API functionality works with SQLite

