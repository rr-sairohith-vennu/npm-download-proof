#!/usr/bin/env python3

"""
Generate verifiable proof of NPM package download statistics
Creates an HTML report that can be saved as PDF for submission
"""

import sys
import json
import urllib.request
from datetime import datetime
import hashlib

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

def generate_verification_hash(package_name, start_date, end_date, downloads, timestamp):
    """Generate a verification hash for the report"""
    data_string = f"{package_name}|{start_date}|{end_date}|{downloads}|{timestamp}"
    return hashlib.sha256(data_string.encode()).hexdigest()[:16]

def generate_html_report(package_name, start_date, end_date, data):
    """Generate HTML proof document"""

    downloads = data['downloads']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    verification_hash = generate_verification_hash(package_name, start_date, end_date, downloads, timestamp)
    verification_url = f"https://api.npmjs.org/downloads/point/{start_date}:{end_date}/{package_name}"
    npm_package_url = f"https://www.npmjs.com/package/{package_name}"
    github_repo = f"https://github.com/Flux159/{package_name}"  # Adjust if needed

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NPM Download Statistics Proof - {package_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
            color: #333;
        }}
        .container {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 40px;
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #cb3837;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #cb3837;
            margin: 0 0 10px 0;
        }}
        .header .subtitle {{
            color: #666;
            font-size: 18px;
        }}
        .stats-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            text-align: center;
            margin: 30px 0;
        }}
        .stats-box .number {{
            font-size: 64px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stats-box .label {{
            font-size: 20px;
            opacity: 0.9;
        }}
        .info-section {{
            margin: 25px 0;
            padding: 20px;
            background: #f8f9fa;
            border-left: 4px solid #cb3837;
            border-radius: 4px;
        }}
        .info-section h3 {{
            margin-top: 0;
            color: #cb3837;
        }}
        .info-row {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }}
        .info-row:last-child {{
            border-bottom: none;
        }}
        .info-label {{
            font-weight: 600;
            color: #555;
        }}
        .info-value {{
            color: #333;
            font-family: 'Courier New', monospace;
        }}
        .verification {{
            background: #e8f5e9;
            border: 2px solid #4caf50;
            border-radius: 8px;
            padding: 20px;
            margin: 30px 0;
        }}
        .verification h3 {{
            color: #2e7d32;
            margin-top: 0;
        }}
        .verification-hash {{
            background: white;
            padding: 10px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            word-break: break-all;
            margin: 10px 0;
        }}
        .links {{
            margin: 30px 0;
        }}
        .link-button {{
            display: inline-block;
            padding: 12px 24px;
            margin: 5px;
            background: #cb3837;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            transition: background 0.3s;
        }}
        .link-button:hover {{
            background: #a02d2d;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 14px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            background: #4caf50;
            color: white;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }}
        @media print {{
            body {{
                background: white;
                margin: 0;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 NPM Download Statistics</h1>
            <div class="subtitle">Official Verification Report</div>
        </div>

        <div class="stats-box">
            <div class="label">Total Downloads</div>
            <div class="number">{downloads:,}</div>
            <div class="label">{start_date} to {end_date}</div>
        </div>

        <div class="info-section">
            <h3>Package Information</h3>
            <div class="info-row">
                <span class="info-label">Package Name:</span>
                <span class="info-value">{package_name}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Start Date:</span>
                <span class="info-value">{data['start']}</span>
            </div>
            <div class="info-row">
                <span class="info-label">End Date:</span>
                <span class="info-value">{data['end']}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Total Downloads:</span>
                <span class="info-value">{downloads:,}</span>
            </div>
        </div>

        <div class="verification">
            <h3>✓ Verification Information</h3>
            <div class="info-row">
                <span class="info-label">Report Generated:</span>
                <span class="info-value">{timestamp}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Data Source:</span>
                <span class="info-value">Official NPM Registry API</span>
            </div>
            <div class="info-row">
                <span class="info-label">Verification Hash:</span>
                <span class="info-value">{verification_hash}</span>
            </div>
            <p style="margin-top: 15px; font-size: 14px;">
                <strong>How to Verify:</strong> Anyone can confirm this data by visiting the API URL below
                or by using the NPM Registry's official download statistics API.
            </p>
        </div>

        <div class="info-section">
            <h3>🔗 Official Links</h3>
            <div style="margin: 15px 0;">
                <div style="margin: 10px 0;">
                    <strong>NPM Package:</strong><br>
                    <a href="{npm_package_url}" target="_blank">{npm_package_url}</a>
                </div>
                <div style="margin: 10px 0;">
                    <strong>API Verification URL:</strong><br>
                    <a href="{verification_url}" target="_blank" style="word-break: break-all; font-size: 12px;">{verification_url}</a>
                </div>
                <div style="margin: 10px 0;">
                    <strong>GitHub Repository:</strong><br>
                    <a href="{github_repo}" target="_blank">{github_repo}</a>
                </div>
            </div>
        </div>

        <div class="info-section">
            <h3>ℹ️ About This Report</h3>
            <p>
                This report contains official download statistics from the NPM Registry API.
                The data represents the total number of times the package "{package_name}"
                was downloaded between {start_date} and {end_date}.
            </p>
            <p>
                <strong>Data Authenticity:</strong> This information is pulled directly from NPM's
                official API endpoint and can be independently verified by anyone using the
                verification URL provided above.
            </p>
        </div>

        <div class="footer">
            <p>
                Generated on {timestamp}<br>
                Data source: <a href="https://api.npmjs.org">NPM Registry API</a><br>
                <span class="badge">OFFICIAL</span> <span class="badge">VERIFIABLE</span>
            </p>
        </div>
    </div>
</body>
</html>"""

    return html

def main():
    if len(sys.argv) < 4:
        print("Usage: python generate_proof.py <package-name> <start-date> <end-date>")
        print("\nExample:")
        print("  python generate_proof.py mcp-server-kubernetes 2025-11-27 2025-12-03")
        print("\nThis will generate an HTML file that can be:")
        print("  - Opened in a browser and saved as PDF (File > Print > Save as PDF)")
        print("  - Submitted as proof of download statistics")
        print("  - Verified by anyone using the API URL in the report")
        sys.exit(1)

    package_name = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]

    print(f"Fetching download statistics for {package_name}...")
    print(f"Period: {start_date} to {end_date}\n")

    data = fetch_downloads(package_name, start_date, end_date)

    if not data:
        print("❌ Failed to fetch download statistics.")
        print("Please check:")
        print("  - Package name is correct")
        print("  - Dates are in YYYY-MM-DD format")
        print("  - You have internet connection")
        sys.exit(1)

    print(f"✓ Successfully fetched data: {data['downloads']:,} downloads\n")

    # Generate HTML report
    html_content = generate_html_report(package_name, start_date, end_date, data)

    # Save to file
    output_filename = f"npm_downloads_proof_{package_name}_{start_date}_to_{end_date}.html"
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✓ Proof document generated: {output_filename}")
    print("\nNext steps:")
    print("  1. Open the HTML file in your web browser")
    print("  2. Save as PDF (File > Print > Save as PDF)")
    print("  3. Submit the PDF as proof of download statistics")
    print("\nThe report includes:")
    print("  ✓ Official download numbers")
    print("  ✓ Verification URL (anyone can confirm the data)")
    print("  ✓ Timestamp of report generation")
    print("  ✓ Verification hash")

if __name__ == "__main__":
    main()
