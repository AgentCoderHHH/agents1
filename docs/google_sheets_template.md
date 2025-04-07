# Google Sheets Template Setup

## Sheet Structure

Create a Google Sheet with the following sheets:

### 1. Website Metrics
```
| Date       | Page Views | Unique Visitors | Avg Time on Page | Bounce Rate | Conversion Rate |
|------------|------------|-----------------|------------------|-------------|-----------------|
| 2024-01-01 | 1000      | 500            | 2.5             | 0.45        | 0.03           |
```

### 2. Twitter Metrics
```
| Date       | Tweet ID | Text           | Retweets | Favorites | Replies | Impressions | Engagement Rate |
|------------|----------|----------------|----------|-----------|---------|-------------|-----------------|
| 2024-01-01 | tweet_1  | Sample tweet 1 | 10       | 20        | 5       | 1000        | 0.035          |
```

### 3. Google Analytics
```
| Date       | Sessions | Users | Pageviews | Avg Session Duration | Goal Completions |
|------------|----------|-------|-----------|---------------------|------------------|
| 2024-01-01 | 800      | 400   | 2000      | 120                 | 10              |
```

## Setup Instructions

1. **Create New Google Sheet**
   - Go to [Google Sheets](https://sheets.google.com)
   - Click "Blank" to create a new spreadsheet
   - Name it "AgentOpenApi Data"

2. **Create Sheets**
   - Click the "+" button at the bottom to add new sheets
   - Rename the sheets to match the template names
   - Copy the header rows from the template

3. **Format Data**
   - Select all cells
   - Format > Number > Automatic
   - For date columns: Format > Number > Date
   - For percentage columns: Format > Number > Percent

4. **Add Sample Data**
   - Copy the sample data from the templates
   - Paste into the respective sheets
   - Ensure dates are in chronological order

5. **Set Up Data Validation**
   - Select the data range (excluding headers)
   - Data > Data Validation
   - For numeric columns: Criteria > Number > greater than or equal to 0
   - For percentage columns: Criteria > Number > between 0 and 1

6. **Share with Service Account**
   - Click "Share" button
   - Add the service account email
   - Set role to "Editor"
   - Uncheck "Notify people"
   - Click "Share"

## Data Collection Automation

The system will automatically:
1. Read data from these sheets
2. Process and clean the data
3. Perform analysis
4. Generate reports
5. Send alerts based on thresholds

## Maintenance

1. **Regular Updates**
   - Add new data daily
   - Keep historical data for trend analysis
   - Archive old data periodically

2. **Data Validation**
   - Check for missing values
   - Verify data ranges
   - Monitor for anomalies

3. **Backup**
   - Export data periodically
   - Keep backup copies
   - Document any changes to the structure 