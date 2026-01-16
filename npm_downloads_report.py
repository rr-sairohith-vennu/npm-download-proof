#!/usr/bin/env python3

"""
Generate NPM package download reports with multiple date ranges
"""

import sys
import json
import urllib.request
from datetime import datetime, timedelta

def fetch_downloads(package_name, start_date, end_date):
    """Fetch download statistics from npm registry"""
    period = f"{start_date}:{end_date}"
    url = f"https://api.npmjs.org/downloads/point/{period}/{package_name}"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data if 'downloads' in data else None
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return None

def get_last_week():
    """Get last 7 days date range"""
    end = datetime.now().date()
    start = end - timedelta(days=7)
    return str(start), str(end)

def get_last_month():
    """Get last 30 days date range"""
    end = datetime.now().date()
    start = end - timedelta(days=30)
    return str(start), str(end)

def get_year_to_date():
    """Get year to date range"""
    end = datetime.now().date()
    start = datetime(end.year, 1, 1).date()
    return str(start), str(end)

def generate_report(package_name, custom_ranges=None):
    """Generate comprehensive download report"""
    print(f"=" * 70)
    print(f"NPM Download Report for: {package_name}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"=" * 70)
    print()

    # Default ranges
    ranges = [
        ("Last 7 Days", get_last_week()),
        ("Last 30 Days", get_last_month()),
        ("Year to Date", get_year_to_date()),
    ]

    # Add custom ranges if provided
    if custom_ranges:
        for label, (start, end) in custom_ranges:
            ranges.append((label, (start, end)))

    results = []

    for label, (start_date, end_date) in ranges:
        print(f"{label} ({start_date} to {end_date}):")
        data = fetch_downloads(package_name, start_date, end_date)

        if data:
            downloads = data['downloads']
            print(f"  ✓ {downloads:,} downloads")
            results.append((label, start_date, end_date, downloads))
        else:
            print(f"  ✗ Failed to fetch data")

        print()

    # Summary table
    if results:
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"{'Period':<20} {'Start Date':<12} {'End Date':<12} {'Downloads':>15}")
        print("-" * 70)

        for label, start, end, downloads in results:
            print(f"{label:<20} {start:<12} {end:<12} {downloads:>15,}")

        print("-" * 70)
        total = sum(d for _, _, _, d in results)
        print(f"{'Note: Periods may overlap':<45} {'':>15}")
        print()

def main():
    if len(sys.argv) < 2:
        print("Usage: python npm_downloads_report.py <package-name> [start-date end-date label]")
        print("\nExamples:")
        print("  # Basic report with last 7 days, 30 days, and YTD")
        print("  python npm_downloads_report.py mcp-server-kubernetes")
        print("\n  # Report with custom date range")
        print("  python npm_downloads_report.py mcp-server-kubernetes 2025-11-27 2025-12-03 \"Custom Week\"")
        sys.exit(1)

    package_name = sys.argv[1]
    custom_ranges = []

    # Parse custom ranges (groups of 3 arguments: start, end, label)
    i = 2
    while i + 2 < len(sys.argv):
        start_date = sys.argv[i]
        end_date = sys.argv[i + 1]
        label = sys.argv[i + 2]
        custom_ranges.append((label, (start_date, end_date)))
        i += 3

    generate_report(package_name, custom_ranges if custom_ranges else None)

if __name__ == "__main__":
    main()
