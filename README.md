## SEO Dashboard & SEO Visualization with Python

## Project Overview

This project involves creating an SEO dashboard for weekly analysis and visualization of SEO data. It consists of two main components:

1. SEO Dashboard Script (seo_dashboard.py)
Extracts and generates the selected weekly SEO data as an Excel file.

2. SEO Visualization Script (seo_dashboard_visual.py)
Reads the generated Excel file and creates meaningful visualizations.

## Setting Up the Project Locally - Initial Configuration

Create a virtual environment with:
python -m venv .venv
and activate it with:
.venv\Scripts\activate

Install the required Python libraries:
pip install pandas matplotlib google-api-python-client google-auth

Get the Credentials.JSON From your Google Search Console Account and add it or replace it to the JSON File

## How to Use the SEO Dashboard

1: In seo_dashboard.py, adjust the start and end dates to match the desired dates.

2:Run seo_dashboard.py:
First activate the virtual environment: .venv\Scripts\activate
Then execute: python -m seo_dashboard.py

3:Add the generated Excel files for the week and history to the global project folder.

4:In seo_dashboard_visual.py, specify the generated Excel files as a string. -> See comments in the code for details.

5:Run the visualization script:
Activate the environment: .venv\Scripts\activate
Then execute: python -m seo_dashboard_visual.py

## INFO 
Several charts will be generated: first, for the top 10 keywords including Clicks, Impressions, and Positions. Next, summarizing all keywords with their Clicks, Impressions, and Positions and finally, charts encompassing the entire Excel File. Each chart is saved twice, once as an image and once as a PDF.
