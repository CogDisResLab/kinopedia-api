\# Deployment Guide



\## Local Development



\### Setup

```cmd

py -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

```



\### Run

```cmd

uvicorn app.main:app --reload

```



Access at: http://localhost:8000



\## Docker Deployment



\### Build

```cmd

docker build -t kinopedia-api .

```



\### Run

```cmd

docker run -p 8000:8000 kinopedia-api

```



\### Docker Compose

```cmd

docker-compose up

```



\## Production Considerations



\### Environment Variables

Create `.env` file:
DATABASE_URL=postgresql+asyncpg://user:password@host/dbname
ENV=production

### Gunicorn (Production Server)
```cmd
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Security
- Set specific CORS origins (not `*`)
- Enable HTTPS
- Set up authentication for POST endpoints
- Use environment variables for sensitive data
- Regular security updates

## Health Check

Endpoint: `GET /health`

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```
