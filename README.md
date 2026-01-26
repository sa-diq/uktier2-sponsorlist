# UK Sponsor License Tracker

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-deployed-brightgreen.svg)

A comprehensive data platform that tracks and analyses UK companies authorised to sponsor work visas, processing 100,000+ sponsor records with automated daily updates.

## Project Overview

The UK government publishes a register of companies licensed to sponsor work visas, but it's just a static CSV file that's difficult to analyse or track over time. This project transforms that raw data into actionable insights through automated ETL pipelines and interactive analytics.

**Key Impact:**
- **100,000+** sponsor companies tracked and analysed
- **Daily automated updates** with change detection
- **Historical trend analysis** of sponsor license additions/removals
- **Zero-maintenance deployment** via GitHub Actions

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GOV.UK CSV    │───▶│   ETL Pipeline   │───▶│   SQLite DB     │
│   (Daily)       │    │   (GitHub        │    │   (Processed    │
└─────────────────┘    │    Actions)      │    │    Data)        │
                       └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Change Log    │    │   Data Cleaning  │    │   Streamlit     │
│   (Daily        │◀───│   & Validation   │    │   Dashboard     │
│   Updates)      │    │                  │    │   (Analytics)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Features

### Automated Data Pipeline
- **Web Scraping**: Automatically fetches the latest sponsor register from GOV.UK
- **Change Detection**: Identifies new sponsors and removes licenses daily  
- **Data Cleaning**: Handles inconsistent city names, missing values, and data validation
- **Historical Tracking**: Maintains a complete audit trail of all changes

### Interactive Analytics Dashboard
- **Real-time Metrics**: Total sponsors, recent additions, growth trends
- **Geographic Analysis**: Sponsor distribution by city and region
- **Visa Route Insights**: Breakdown by Worker, Temporary Worker categories
- **Time Series Analysis**: Daily/weekly/monthly trending with custom date ranges

### Advanced Filtering & Search
- **Full-text Search**: Find specific companies across 100k+ records
- **Multi-dimensional Filtering**: By location, visa route, date added
- **Export Capabilities**: Filtered results for further analysis

## Technical Stack

- **Backend**: Python, pandas, SQLite, BeautifulSoup
- **Frontend**: Streamlit with custom CSS/responsive design  
- **Automation**: GitHub Actions (scheduled daily runs)
- **Deployment**: Streamlit Cloud
- **Data Processing**: ETL pipelines with error handling and logging



## Impact & Use Cases

- **Job Seekers**: Identify companies that can sponsor work visas
- **Immigration Professionals**: Track sponsor license changes
- **Recruitment Agencies**: Monitor new opportunities for visa-requiring candidates
- **Policy Researchers**: Analyse trends in UK immigration and business licensing

## Future Enhancements

- [ ] Company categorisation by industry/sector
- [ ] Email alerts for new sponsors in specific locations
- [ ] API endpoints for programmatic access
- [ ] Integration with job boards for sponsor verification
- [ ] Machine learning for sponsor license duration prediction

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Data source: [GOV.UK Register of Licensed Sponsors](https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers)
- Built with [Streamlit](https://streamlit.io/) for rapid dashboard development

---

**Live Dashboard**: [https://uksponsorlist.streamlit.app/]

*This project demonstrates end-to-end data engineering capabilities, including web scraping, ETL pipeline design, automated workflows, data analytics, and modern web application development.*
