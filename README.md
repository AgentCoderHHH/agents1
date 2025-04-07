# Agent System

A comprehensive agent-based system for managing goals, tasks, and progress tracking with AI-powered assistance.

## Features

- **Goal Management**: Create, track, and manage organizational goals
- **Task Management**: Assign, track, and manage tasks with dependencies
- **Progress Tracking**: Monitor progress towards goals and tasks
- **AI Integration**: Leverage OpenAI's GPT models for intelligent assistance
- **Data Management**: Store and manage data in MongoDB and PostgreSQL
- **API Support**: REST and GraphQL APIs for flexible integration
- **Security**: JWT-based authentication and role-based authorization
- **Caching**: Efficient data caching for improved performance

## Architecture

The system is built with a modular architecture:

- **Agents**: Specialized components for different functionalities
  - **Management Agents**
    - Progress Tracker Agent: Monitors and reports on goal progress
    - Goal Alignment Agent: Ensures alignment with organizational objectives
    - Task Management Agent: Manages task assignments and dependencies
  - **Research Agents**
    - Internet Documentation Agent: Handles web research and content extraction
    - Documentation Maker Agent: Generates and structures documentation
    - Prompt Engineering Agent: Optimizes AI interactions
  - **Analytics Agents**
    - Data Analysis Agent: Processes and analyzes data
    - Performance Tracking Agent: Monitors system performance
  - **Community Agents**
    - Community Manager Agent: Manages community interactions
    - Feedback Agent: Collects and processes user feedback
  - **Documentation Agents**
    - Documentation Generator Agent: Creates technical documentation
    - Knowledge Base Agent: Maintains and updates knowledge base

- **Data Sources**: Support for multiple data storage options
  - MongoDB for document storage
  - PostgreSQL for relational data

- **APIs**: Multiple interface options
  - REST API for traditional integration
  - GraphQL API for flexible querying

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/agent-system.git
   cd agent-system
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your configuration.

5. Set up databases:
   - Install and configure MongoDB
   - Install and configure PostgreSQL
   - Create the necessary databases and users

## Usage

1. Start the server:
   ```bash
   python -m agents.main
   ```

2. Access the APIs:
   - REST API: http://localhost:8000/api/docs
   - GraphQL API: http://localhost:8000/graphql

3. Example API calls:

   **REST API**:
   ```bash
   # Create a goal
   curl -X POST "http://localhost:8000/api/goals" \
     -H "Authorization: Bearer your_token" \
     -H "Content-Type: application/json" \
     -d '{"title": "Project Completion", "description": "Complete the project on time"}'

   # Get goals
   curl "http://localhost:8000/api/goals" \
     -H "Authorization: Bearer your_token"
   ```

   **GraphQL API**:
   ```graphql
   # Create a goal
   mutation {
     createGoal(
       title: "Project Completion"
       description: "Complete the project on time"
     ) {
       id
       title
       status
     }
   }

   # Get goals
   query {
     goals {
       id
       title
       status
     }
   }
   ```

## Development

1. Set up development environment:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Run linter:
   ```bash
   flake8
   ```

4. Run type checker:
   ```bash
   mypy .
   ```

## Security

- All API endpoints require authentication
- JWT tokens are used for authentication
- Role-based access control is implemented
- Passwords are hashed using bcrypt
- CORS is configured for security

## Monitoring

- Logs are stored in `logs/agent_system.log`
- System status can be checked via the `/api/status` endpoint
- Performance metrics are available through the analytics agent

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 