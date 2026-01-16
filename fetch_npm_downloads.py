#!/usr/bin/env python3

"""
Fetch NPM package download statistics for a specific date range
API: https://api.npmjs.org/downloads/point/{period}/{package}
"""

import sys
import json
import urllib.request
from datetime import datetime

def fetch_downloads(package_name, start_date, end_date):
    """Fetch download statistics from npm registry"""
    period = f"{start_date}:{end_date}"
    url = f"https://api.npmjs.org/downloads/point/{period}/{package_name}"

    print(f"Fetching downloads for {package_name} from {start_date} to {end_date}...")
    print(f"URL: {url}\n")

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

            if 'downloads' in data:
                print("✓ Success!")
                print(f"Package: {data['package']}")
                print(f"Period: {data['start']} to {data['end']}")
                print(f"Total Downloads: {data['downloads']:,}")
                return data
            else:
                print("Response:", data)
                return None

    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def validate_date(date_string):
    """Validate date format YYYY-MM-DD"""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def main():
    if len(sys.argv) < 4:
        print("Usage: python fetch_npm_downloads.py <package-name> <start-date> <end-date>")
        print("Date format: YYYY-MM-DD")
        print("\nExample:")
        print("  python fetch_npm_downloads.py mcp-server-kubernetes 2025-11-27 2025-12-03")
        sys.exit(1)

    package_name = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]

    # Validate dates
    if not validate_date(start_date) or not validate_date(end_date):
        print("Error: Dates must be in YYYY-MM-DD format")
        sys.exit(1)

    fetch_downloads(package_name, start_date, end_date)

if __name__ == "__main__":
    main()
