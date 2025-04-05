# Agent OpenAI Project

This project uses OpenAI's GPT models for various documentation and technical analysis tasks.

## Setup

1. Clone the repository
```bash
git clone <repository-url>
cd AgentOpenApi
```

2. Install dependencies
```bash
npm install
```

3. Configure environment variables
- Copy `.env.example` to `.env`
```bash
cp .env.example .env
```
- Edit `.env` and add your OpenAI API key and other configuration

4. Start the development server
```bash
npm run dev
```

## Environment Variables

The following environment variables are required:

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: The OpenAI model to use (default: gpt-4)
- `OPENAI_MAX_TOKENS`: Maximum tokens for API calls (default: 2000)
- `OPENAI_TEMPERATURE`: Temperature for response generation (default: 0.7)
- `PORT`: Server port (default: 3001)
- `NODE_ENV`: Environment (development/production)

## Security Notes

- Never commit the `.env` file
- Always use `.env.example` for documenting required environment variables
- Keep your API keys secure and rotate them regularly
- Use environment-specific settings for different deployment environments 