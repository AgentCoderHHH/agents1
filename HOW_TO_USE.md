# How to Use the Agent System

This guide will walk you through setting up and using the Agent System for goal tracking, task management, and progress monitoring.

## Table of Contents
1. [Environment Setup](#1-environment-setup)
2. [System Configuration](#2-system-configuration)
3. [Running the System](#3-running-the-system)
4. [Real-World Usage Examples](#4-real-world-usage-examples)
5. [API Usage](#5-api-usage)
6. [Monitoring and Maintenance](#6-monitoring-and-maintenance)

## 1. Environment Setup

### 1.1 Required Services

#### OpenAI API Setup
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an account or log in
3. Navigate to API keys section
4. Create a new API key
5. Copy the API key

#### MongoDB Setup
Option 1: Local Installation
1. Download MongoDB Community Server from [MongoDB](https://www.mongodb.com/try/download/community)
2. Install MongoDB following the installation wizard
3. Start MongoDB service
4. Verify installation by running `mongod --version`

Option 2: MongoDB Atlas (Cloud)
1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Set up database access (username/password)
4. Set up network access (IP whitelist)
5. Get connection string from "Connect" button

#### PostgreSQL Setup
Option 1: Local Installation
1. Download PostgreSQL from [PostgreSQL](https://www.postgresql.org/download/)
2. Install PostgreSQL following the installation wizard
3. Set up password for postgres user
4. Start PostgreSQL service
5. Verify installation by running `psql --version`

Option 2: Cloud Service
1. Sign up for a cloud PostgreSQL service (e.g., ElephantSQL, Heroku Postgres)
2. Create a new database
3. Get connection string

### 1.2 Python Environment Setup

1. Create and activate virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 2. System Configuration

1. Copy environment template:
```bash
cp .env.example .env
```

2. Edit `.env` file with your configurations:
```env
# OpenAI Configuration
OPENAI_API_KEY=your_api_key_here

# Database Configuration
MONGODB_URI=mongodb://localhost:27017/agent_system
# OR for Atlas
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/agent_system

POSTGRES_URI=postgresql://username:password@localhost:5432/agent_system

# Server Configuration
PORT=8000
HOST=0.0.0.0
DEBUG=True

# Security Configuration
JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/agent_system.log
LOG_RETENTION_DAYS=7
```

## 3. Running the System

1. Start the server:
```bash
python -m agents.main
```

2. Verify the system is running:
- Open browser and navigate to http://localhost:8000
- You should see the API documentation

3. Access APIs:
- REST API Documentation: http://localhost:8000/api/docs
- GraphQL Playground: http://localhost:8000/graphql

## 4. Real-World Usage Examples

### 4.1 Project Management Scenario

1. Create Project Goals:
```bash
# Create main project goal
curl -X POST "http://localhost:8000/api/goals" \
  -H "Authorization: Bearer your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Develop E-commerce Platform",
    "description": "Build a full-featured e-commerce platform",
    "deadline": "2024-06-30",
    "priority": "high"
  }'

# Create sub-goals
curl -X POST "http://localhost:8000/api/goals" \
  -H "Authorization: Bearer your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "User Management System",
    "description": "Implement user registration and authentication",
    "deadline": "2024-04-15",
    "priority": "high",
    "parent_goal_id": "main_goal_id"
  }'
```

2. Create Tasks:
```bash
# Create task for User Management System
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Authorization: Bearer your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Design User Database Schema",
    "description": "Create database tables for user data",
    "assignee": "backend_team",
    "priority": "high",
    "goal_id": "user_management_goal_id"
  }'
```

3. Update Task Progress:
```bash
# Update task status
curl -X PUT "http://localhost:8000/api/tasks/task_id/status" \
  -H "Authorization: Bearer your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress",
    "progress": 60,
    "blockers": ["Waiting for database schema approval"]
  }'
```

### 4.2 Team Performance Tracking

1. Create Team Goals:
```bash
curl -X POST "http://localhost:8000/api/goals" \
  -H "Authorization: Bearer your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Improve Team Velocity",
    "description": "Increase team velocity by 20%",
    "metrics": {
      "target_velocity": 40,
      "current_velocity": 33
    }
  }'
```

2. Track Team Progress:
```bash
# Get team progress report
curl -X GET "http://localhost:8000/api/progress/team_report" \
  -H "Authorization: Bearer your_token"
```

## 5. API Usage

### 5.1 REST API Endpoints

1. Goals Management:
- `POST /api/goals` - Create new goal
- `GET /api/goals` - List all goals
- `GET /api/goals/{goal_id}` - Get goal details
- `PUT /api/goals/{goal_id}` - Update goal
- `DELETE /api/goals/{goal_id}` - Delete goal

2. Tasks Management:
- `POST /api/tasks` - Create new task
- `GET /api/tasks` - List all tasks
- `GET /api/tasks/{task_id}` - Get task details
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task

3. Progress Tracking:
- `GET /api/progress/goals` - Get goals progress
- `GET /api/progress/tasks` - Get tasks progress
- `GET /api/progress/team_report` - Get team progress report

### 5.2 GraphQL API

Example Queries:
```graphql
# Get goals with progress
query {
  goals {
    id
    title
    status
    progress {
      percentage
      lastUpdated
    }
  }
}

# Get tasks with dependencies
query {
  tasks {
    id
    title
    status
    dependencies {
      id
      title
    }
  }
}
```

## 6. Monitoring and Maintenance

### 6.1 System Monitoring

1. Check Logs:
```bash
# View system logs
tail -f logs/agent_system.log
```

2. Monitor System Health:
```bash
# Check system status
curl -X GET "http://localhost:8000/api/status" \
  -H "Authorization: Bearer your_token"
```

### 6.2 Data Maintenance

1. Backup Database:
```bash
# Backup MongoDB
mongodump --uri="your_mongodb_uri" --out=backups/

# Backup PostgreSQL
pg_dump "your_postgres_uri" > backup.sql
```

2. Clean Up Old Data:
```bash
# Archive completed goals older than 6 months
curl -X POST "http://localhost:8000/api/maintenance/archive" \
  -H "Authorization: Bearer your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "older_than": "6 months"
  }'
```

### 6.3 Troubleshooting

1. Check Agent Status:
```bash
# Get agent status
curl -X GET "http://localhost:8000/api/agents/status" \
  -H "Authorization: Bearer your_token"
```

2. View Error Logs:
```bash
# Check error logs
grep "ERROR" logs/agent_system.log
```

3. Restart Services:
```bash
# Restart the server
python -m agents.main
```

For additional support or questions, please refer to the documentation or create an issue in the repository. 