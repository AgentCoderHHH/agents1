# Credentials Security Guide

## Overview
This document outlines the security measures in place for handling sensitive credentials in the AgentOpenApi project.

## Credentials Storage
All sensitive credentials are stored in two locations:
1. `.env` file for environment variables
2. `config/credentials/credentials.json` for Google Sheets service account credentials

## Security Measures
1. **Git Ignore**
   - Both `.env` and `credentials.json` are ignored by Git
   - Example files (`.env.example` and `credentials.example.json`) are provided
   - Never commit actual credentials to version control

2. **Directory Structure**
   ```
   config/
   └── credentials/
       ├── credentials.json        # Actual credentials (gitignored)
       └── credentials.example.json # Example template
   ```

3. **Environment Variables**
   - All sensitive API keys and tokens are stored in `.env`
   - The file is loaded using `python-dotenv`
   - Environment variables are validated before use

4. **Google Sheets Credentials**
   - Service account credentials are stored in `credentials.json`
   - The file is validated for required fields
   - Credentials are loaded securely using the Config class

## Setup Instructions
1. Copy the example files:
   ```bash
   cp .env.example .env
   cp config/credentials/credentials.example.json config/credentials/credentials.json
   ```

2. Fill in the credentials:
   - Update `.env` with your actual environment variables
   - Update `credentials.json` with your Google service account credentials

3. Verify the setup:
   ```python
   from agents.config import Config
   Config.validate_config()  # Should return True
   ```

## Security Best Practices
1. Never commit credentials to version control
2. Use strong, unique passwords and API keys
3. Regularly rotate credentials
4. Limit service account permissions to minimum required
5. Use environment-specific credentials (development, staging, production)
6. Monitor for unauthorized access
7. Keep credentials files in a secure location
8. Use encryption for sensitive data when possible

## Emergency Procedures
If credentials are compromised:
1. Immediately rotate all affected credentials
2. Revoke compromised API keys
3. Update the credentials files
4. Notify affected team members
5. Review access logs for suspicious activity

## Additional Resources
- [Google Cloud Security](https://cloud.google.com/security)
- [Python Security Best Practices](https://docs.python.org/3/security.html)
- [OWASP Security Guidelines](https://owasp.org/www-project-top-ten/) 