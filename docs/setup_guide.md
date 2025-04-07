# Setup Guide

## Environment Setup

1. **Create a Python Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create Environment Variables File**
   Create a `.env` file in the project root with the following structure:
   ```
   # Google Sheets Configuration
   GOOGLE_SHEETS_CREDENTIALS_PATH=path/to/credentials.json
   GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id

   # Twitter API Configuration
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET=your_api_secret
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret

   # Telegram Bot Configuration
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

## Google Sheets Service Account Setup

1. **Create a Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click "Create Project" or select an existing project
   - Give your project a name and click "Create"

2. **Enable Google Sheets API**
   - In the Google Cloud Console, go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

3. **Create Service Account**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in the service account details:
     - Name: `agent-openapi`
     - ID: `agent-openapi`
     - Description: "Service account for AgentOpenApi project"
   - Click "Create and Continue"
   - Skip role assignment (we'll do this later)
   - Click "Done"

4. **Create and Download Service Account Key**
   - In the service accounts list, find your new service account
   - Click on the service account email
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose "JSON" format
   - Click "Create"
   - The key file will download automatically
   - Move the downloaded JSON file to your project's `config` directory
   - Rename it to `google_sheets_credentials.json`

5. **Share Google Sheet with Service Account**
   - Open your Google Sheet
   - Click "Share" button
   - Add the service account email (found in the JSON file as `client_email`)
   - Give it "Editor" access
   - Click "Done"

6. **Get Spreadsheet ID**
   - Open your Google Sheet
   - The spreadsheet ID is in the URL: `https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit`
   - Copy the ID and add it to your `.env` file

## Testing the Setup

1. **Verify Google Sheets Access**
   ```python
   from agents.data import GoogleAnalyticsFetcherAgent
   
   fetcher = GoogleAnalyticsFetcherAgent()
   data = fetcher.fetch_data()
   print(data)
   ```

2. **Run Unit Tests**
   ```bash
   python tests/run_tests.py
   ```

3. **Run Integration Tests**
   ```bash
   python -m unittest tests/test_integration.py
   ```

## Troubleshooting

1. **Google Sheets Access Issues**
   - Verify the service account email has access to the spreadsheet
   - Check if the credentials file path is correct in `.env`
   - Ensure the spreadsheet ID is correct

2. **API Rate Limits**
   - Google Sheets API has rate limits
   - Implement exponential backoff in your code
   - Monitor usage in Google Cloud Console

3. **Authentication Errors**
   - Check if the credentials file is valid
   - Verify the service account is properly set up
   - Ensure all required APIs are enabled

## Security Best Practices

1. **Credentials Security**
   - Never commit credentials to version control
   - Use environment variables for sensitive data
   - Regularly rotate service account keys

2. **Access Control**
   - Follow principle of least privilege
   - Regularly audit service account permissions
   - Remove unused service accounts

3. **Data Protection**
   - Encrypt sensitive data
   - Implement proper error handling
   - Log security-relevant events 