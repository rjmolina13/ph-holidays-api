# Philippines Public Holidays API

An automated system that scrapes Philippines public holidays from [publicholidays.ph](https://publicholidays.ph) and converts them to a structured XML format with MM-DD date formatting.

## Features

- 🔄 **Auto-updating**: GitHub Actions workflow runs daily to fetch the latest holiday data
- 📅 **MM-DD Format**: Converts dates to MM-DD format for easy integration
- 🌐 **XML API**: Outputs structured XML that can be consumed as an API
- 🇵🇭 **Philippines Focus**: Specifically designed for Philippine public holidays
- ⚙️ **Configurable**: URL source can be changed via environment variables

## Files

- `scrape_holidays.py` - Python script that scrapes holiday data and generates XML
- `ph_holidays.xml` - Generated XML file with holiday data (auto-updated)
- `.github/workflows/update-holidays.yml` - GitHub Actions workflow for automation
- `requirements.txt` - Python dependencies

## Usage

### Manual Execution

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the scraper:
   ```bash
   python scrape_holidays.py
   ```

### Environment Variables

- `HOLIDAYS_URL`: Source URL to scrape (default: `https://publicholidays.ph/2025-dates/`)
- `OUTPUT_FILE`: Output XML filename (default: `ph_holidays.xml`)

### GitHub Actions

The workflow automatically:
- Runs daily at 6 AM UTC (2 PM PHT)
- Can be triggered manually
- Runs on pushes to main/master branch
- Commits updated XML file back to the repository

## XML Structure

The generated XML follows this structure:

```xml
<?xml version='1.0' encoding='utf-8'?>
<holidays year="2025" country="Philippines" last_updated="2025-07-30T12:36:20.210509">
  <holiday>
    <date>1 Jan</date>
    <day>Wed</day>
    <name>New Year's Day</name>
    <mm_dd>01-01</mm_dd>
  </holiday>
  <!-- More holidays... -->
</holidays>
```

## API Usage

Once deployed, you can use the XML file as a simple API:

```bash
# Get all holidays
curl https://raw.githubusercontent.com/yourusername/ph-holidays-api/main/ph_holidays.xml
```

## Holiday Data

The system captures the following Philippine holidays:
- New Year's Day
- Chinese New Year
- Maundy Thursday, Good Friday, Black Saturday
- Day of Valor (Araw ng Kagitingan)
- Labor Day
- Independence Day
- Eidul Fitr and Eidul Adha
- Ninoy Aquino Day
- National Heroes Day
- All Saints' Day
- Bonifacio Day
- Immaculate Conception
- Christmas holidays
- Rizal Day
- And more...

## Contributing

1. Fork the repository
2. Make your changes
3. Test the scraper script
4. Submit a pull request

## License

This project is open source. The holiday data is sourced from [publicholidays.ph](https://publicholidays.ph).