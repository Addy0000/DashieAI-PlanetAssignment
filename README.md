# Dashie - AI Strategy Analysis Platform

## Overview
Dashie is a Streamlit-based web application that provides automated company analysis and AI strategy recommendations. It combines market research, industry analysis, and resource discovery to generate comprehensive strategic reports.

## Features
- Automated industry classification
- Market research and trend analysis
- AI/ML use case generation
- Dataset resource mapping
- Interactive dashboard
- Downloadable reports

## Technology Stack
- Python
- Streamlit
- OpenAI GPT-4
- Exa API
- AutoGen

## Installation

```bash
# Clone the repository
git clone https://github.com/Addy0000/DashieAI-PlanetAssignment.git

# Navigate to project directory
cd DashieAI-PlanetAssignment

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:
```
EXA_API_KEY=your_exa_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Enter a company name in the search field
3. Click "Generate Analysis"
4. View results across four tabs:
   - Market Research
   - Strategic Use Cases
   - Resources
   - Full Report
5. Demo Video :

## Project Structure
```
dashie/
├── app.py              # Main application file
├── dashie.svg          # Logo file
├── requirements.txt    # Project dependencies
└── .env               # Environment variables
```

## Dependencies
- streamlit
- exa-py
- autogen
- python-dotenv

## Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License
MIT License

## Author
Created by Adarsh
