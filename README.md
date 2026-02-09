# ECS Demo Flask Application

A Flask web application with MongoDB integration for managing items with CRUD operations. Designed to run in AWS ECS containers.

## Features

- Modern responsive UI with gradient styling
- CRUD operations for items with prices and dynamic fields
- MongoDB integration with health checks
- REST API endpoints
- Docker ready

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Start MongoDB
docker run -d -p 27017:27017 --name mongodb mongo:6

# Run application
python app.py
```

Access at `http://localhost:80`

### Docker Deployment

```bash
# Using Docker Compose
docker-compose up -d

# Or build and run manually
docker build -t ecs-demo-app .
docker run -d -p 80:80 --link mongodb:mongodb -e MONGO_HOST=mongodb ecs-demo-app
```

## Configuration

Environment variables:

- `MONGO_HOST` - MongoDB hostname (default: `localhost`)
- `MONGO_PORT` - MongoDB port (default: `27017`)
- `MONGO_DB` - Database name (default: `ecs_demo`)

## API Endpoints

- `GET /` - Web UI
- `GET /health` - Health check
- `GET /api/items` - Get all items (JSON)
- `POST /add` - Add new item
- `POST /delete/<item_id>` - Delete item

## Project Structure

```
ecs-app/
├── app.py              # Flask application
├── requirements.txt    # Dependencies
├── Dockerfile         # Container definition
├── templates/
│   └── index.html     # UI template
└── static/
    └── css/
        └── style.css  # Styles
```

## AWS ECS Deployment

```bash
# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker build -t <ecr-repo>:latest .
docker push <ecr-repo>:latest

# Deploy with Terraform (from ecs-infra directory)
terraform apply -var="frontend_image=<ecr-repo>:latest"
```
