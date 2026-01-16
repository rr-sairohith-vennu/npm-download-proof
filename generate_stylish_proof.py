#!/usr/bin/env python3

"""
Generate a beautifully designed, Apple-style proof document with interactive charts
Clean white and light gray design
"""

import sys
import json
import urllib.request
from datetime import datetime, timedelta
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

def fetch_range_data(package_name, start_date, end_date):
    """Fetch daily download data for charts"""
    period = f"{start_date}:{end_date}"
    url = f"https://api.npmjs.org/downloads/range/{period}/{package_name}"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data if 'downloads' in data else None
    except Exception as e:
        return None

def calculate_weekly_data(daily_data):
    """Aggregate daily data into weekly data"""
    if not daily_data:
        return []

    weekly = []
    current_week = []
    current_week_downloads = 0

    for entry in daily_data:
        current_week.append(entry)
        current_week_downloads += entry['downloads']

        # If we have 7 days, create a week entry
        if len(current_week) == 7:
            week_start = current_week[0]['day']
            week_end = current_week[-1]['day']
            weekly.append({
                'start': week_start,
                'end': week_end,
                'downloads': current_week_downloads,
                'label': f"{week_start[5:]}"
            })
            current_week = []
            current_week_downloads = 0

    # Add remaining days as a partial week
    if current_week:
        week_start = current_week[0]['day']
        week_end = current_week[-1]['day']
        weekly.append({
            'start': week_start,
            'end': week_end,
            'downloads': current_week_downloads,
            'label': f"{week_start[5:]}"
        })

    return weekly

def calculate_monthly_data(daily_data):
    """Aggregate daily data into monthly data"""
    if not daily_data:
        return []

    monthly = {}

    for entry in daily_data:
        month_key = entry['day'][:7]  # YYYY-MM
        if month_key not in monthly:
            monthly[month_key] = {
                'month': month_key,
                'downloads': 0,
                'label': datetime.strptime(month_key, '%Y-%m').strftime('%b %Y')
            }
        monthly[month_key]['downloads'] += entry['downloads']

    return list(monthly.values())

def generate_verification_hash(package_name, start_date, end_date, downloads, timestamp):
    """Generate a verification hash for the report"""
    data_string = f"{package_name}|{start_date}|{end_date}|{downloads}|{timestamp}"
    return hashlib.sha256(data_string.encode()).hexdigest()[:16]

def generate_html_report(package_name, start_date, end_date, data, range_data=None):
    """Generate beautiful Apple-style HTML proof document"""

    downloads = data['downloads']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    verification_hash = generate_verification_hash(package_name, start_date, end_date, downloads, timestamp)
    verification_url = f"https://api.npmjs.org/downloads/point/{start_date}:{end_date}/{package_name}"
    npm_package_url = f"https://www.npmjs.com/package/{package_name}"
    github_repo = f"https://github.com/Flux159/{package_name}"

    # Prepare chart data
    daily_data = range_data.get('downloads', []) if range_data else []
    weekly_data = calculate_weekly_data(daily_data)
    monthly_data = calculate_monthly_data(daily_data)

    # Convert to JSON for JavaScript
    daily_json = json.dumps(daily_data)
    weekly_json = json.dumps(weekly_data)
    monthly_json = json.dumps(monthly_data)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NPM Download Statistics - {package_name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --primary-text: #1d1d1f;
            --secondary-text: #6e6e73;
            --background: #ffffff;
            --surface: #f5f5f7;
            --border: #d2d2d7;
            --accent: #000000;
            --card-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            --card-hover-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--surface);
            color: var(--primary-text);
            line-height: 1.6;
            min-height: 100vh;
            overflow-x: hidden;
        }}

        .hero {{
            background: var(--background);
            border-bottom: 1px solid var(--border);
            padding: 80px 20px;
            text-align: center;
        }}

        .hero-content {{
            max-width: 900px;
            margin: 0 auto;
            animation: fadeInUp 0.8s ease-out;
        }}

        .hero h1 {{
            font-size: 56px;
            font-weight: 600;
            margin-bottom: 16px;
            letter-spacing: -1px;
            color: var(--primary-text);
        }}

        .hero .subtitle {{
            font-size: 24px;
            font-weight: 400;
            color: var(--secondary-text);
            animation: fadeInUp 0.8s ease-out 0.2s both;
        }}

        .package-name {{
            display: inline-block;
            background: var(--surface);
            padding: 12px 28px;
            border-radius: 24px;
            font-size: 18px;
            font-weight: 500;
            margin-top: 24px;
            color: var(--primary-text);
            animation: fadeInUp 0.8s ease-out 0.4s both;
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 60px 20px 80px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            background: var(--background);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 36px 32px;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: fadeInUp 0.6s ease-out both;
        }}

        .stat-card:nth-child(1) {{ animation-delay: 0.1s; }}
        .stat-card:nth-child(2) {{ animation-delay: 0.2s; }}
        .stat-card:nth-child(3) {{ animation-delay: 0.3s; }}

        .stat-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--card-hover-shadow);
        }}

        .stat-label {{
            font-size: 13px;
            font-weight: 600;
            color: var(--secondary-text);
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin-bottom: 16px;
        }}

        .stat-value {{
            font-size: 52px;
            font-weight: 600;
            color: var(--primary-text);
            line-height: 1;
            letter-spacing: -1px;
        }}

        .chart-section {{
            background: var(--background);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 48px 40px;
            margin-bottom: 24px;
            animation: fadeInUp 0.6s ease-out 0.4s both;
        }}

        .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            flex-wrap: wrap;
            gap: 20px;
        }}

        .chart-title {{
            font-size: 32px;
            font-weight: 600;
            color: var(--primary-text);
            letter-spacing: -0.5px;
        }}

        .chart-tabs {{
            display: flex;
            gap: 0;
            background: var(--surface);
            padding: 3px;
            border-radius: 10px;
        }}

        .chart-tab {{
            padding: 10px 24px;
            border: none;
            background: transparent;
            color: var(--secondary-text);
            font-size: 14px;
            font-weight: 500;
            border-radius: 7px;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .chart-tab:hover {{
            color: var(--primary-text);
        }}

        .chart-tab.active {{
            background: var(--background);
            color: var(--primary-text);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}

        .chart-container {{
            position: relative;
            height: 380px;
            margin-bottom: 20px;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
            margin-bottom: 24px;
        }}

        .info-card {{
            background: var(--background);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 36px;
            animation: fadeInUp 0.6s ease-out both;
        }}

        .info-card:nth-child(1) {{ animation-delay: 0.5s; }}
        .info-card:nth-child(2) {{ animation-delay: 0.6s; }}

        .info-card h3 {{
            font-size: 20px;
            font-weight: 600;
            color: var(--primary-text);
            margin-bottom: 24px;
        }}

        .info-row {{
            display: flex;
            justify-content: space-between;
            padding: 18px 0;
            border-bottom: 1px solid var(--surface);
            align-items: flex-start;
            gap: 20px;
        }}

        .info-row:last-child {{
            border-bottom: none;
        }}

        .info-label {{
            font-size: 14px;
            font-weight: 500;
            color: var(--secondary-text);
            flex-shrink: 0;
        }}

        .info-value {{
            font-size: 14px;
            font-weight: 500;
            color: var(--primary-text);
            font-family: 'SF Mono', 'Monaco', monospace;
            text-align: right;
            word-break: break-word;
        }}

        .verification-card {{
            background: var(--background);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 36px;
            animation: fadeInUp 0.6s ease-out 0.7s both;
        }}

        .verification-card h3 {{
            font-size: 20px;
            font-weight: 600;
            color: var(--primary-text);
            margin-bottom: 20px;
        }}

        .verification-card p {{
            color: var(--secondary-text);
            line-height: 1.8;
            margin-bottom: 24px;
        }}

        .badge {{
            display: inline-block;
            padding: 6px 16px;
            background: var(--primary-text);
            color: var(--background);
            border-radius: 16px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }}

        .link-button {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 14px 28px;
            background: var(--primary-text);
            color: var(--background);
            text-decoration: none;
            border-radius: 12px;
            font-weight: 500;
            font-size: 15px;
            transition: all 0.2s;
        }}

        .link-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
        }}

        .link-button.secondary {{
            background: var(--background);
            color: var(--primary-text);
            border: 1px solid var(--border);
        }}

        .link-button.secondary:hover {{
            background: var(--surface);
        }}

        .links-section {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 24px;
        }}

        .api-endpoint {{
            margin-top: 20px;
            padding: 20px;
            background: var(--surface);
            border-radius: 12px;
            font-size: 12px;
            font-family: 'SF Mono', 'Monaco', monospace;
            word-break: break-all;
            color: var(--secondary-text);
            line-height: 1.6;
        }}

        .api-endpoint strong {{
            color: var(--primary-text);
            display: block;
            margin-bottom: 8px;
        }}

        .footer {{
            text-align: center;
            padding: 60px 20px 40px;
            color: var(--secondary-text);
            font-size: 13px;
            border-top: 1px solid var(--border);
        }}

        .footer a {{
            color: var(--primary-text);
            text-decoration: none;
        }}

        .footer a:hover {{
            text-decoration: underline;
        }}

        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 40px;
            }}

            .hero .subtitle {{
                font-size: 20px;
            }}

            .stat-value {{
                font-size: 42px;
            }}

            .chart-container {{
                height: 280px;
            }}

            .chart-title {{
                font-size: 24px;
            }}
        }}

        @media print {{
            body {{
                background: white;
            }}

            .stat-card, .chart-section, .info-card, .verification-card {{
                box-shadow: none;
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="hero">
        <div class="hero-content">
            <h1>Download Statistics</h1>
            <p class="subtitle">Official NPM Registry Verification</p>
            <div class="package-name">{package_name}</div>
        </div>
    </div>

    <div class="container">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Downloads</div>
                <div class="stat-value">{downloads:,}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Start Date</div>
                <div class="stat-value" style="font-size: 28px;">{data['start']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">End Date</div>
                <div class="stat-value" style="font-size: 28px;">{data['end']}</div>
            </div>
        </div>

        <div class="chart-section" id="chartSection" style="display: {'block' if daily_data else 'none'};">
            <div class="chart-header">
                <h2 class="chart-title">Download Trends</h2>
                <div class="chart-tabs">
                    <button class="chart-tab active" onclick="showChart('daily', event)">Daily</button>
                    <button class="chart-tab" onclick="showChart('weekly', event)" id="weeklyTab" style="display: {'inline-block' if len(weekly_data) > 1 else 'none'};">Weekly</button>
                    <button class="chart-tab" onclick="showChart('monthly', event)" id="monthlyTab" style="display: {'inline-block' if len(monthly_data) > 1 else 'none'};">Monthly</button>
                </div>
            </div>
            <div class="chart-container">
                <canvas id="downloadChart"></canvas>
            </div>
        </div>

        <div class="info-grid">
            <div class="info-card">
                <h3>Package Information</h3>
                <div class="info-row">
                    <span class="info-label">Package Name</span>
                    <span class="info-value">{package_name}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Date Range</span>
                    <span class="info-value">{data['start']} to {data['end']}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Total Downloads</span>
                    <span class="info-value">{downloads:,}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Report Generated</span>
                    <span class="info-value">{timestamp}</span>
                </div>
            </div>

            <div class="info-card">
                <h3>Verification</h3>
                <div class="info-row">
                    <span class="info-label">Data Source</span>
                    <span class="info-value">NPM Registry API</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Verification Hash</span>
                    <span class="info-value">{verification_hash}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Status</span>
                    <span class="info-value"><span class="badge">VERIFIED</span></span>
                </div>
            </div>
        </div>

        <div class="verification-card">
            <h3>How to Verify This Data</h3>
            <p>
                This report contains official data from the NPM Registry API. Anyone can independently
                verify these statistics by visiting the API endpoint below or checking the NPM package page.
            </p>
            <div class="links-section">
                <a href="{npm_package_url}" class="link-button" target="_blank">
                    View on NPM
                </a>
                <a href="{github_repo}" class="link-button secondary" target="_blank">
                    GitHub Repository
                </a>
            </div>
            <div class="api-endpoint">
                <strong>API Endpoint</strong>
                {verification_url}
            </div>
        </div>
    </div>

    <div class="footer">
        <p>
            Generated on {timestamp}<br>
            Data source: <a href="https://api.npmjs.org" target="_blank">NPM Registry API</a>
        </p>
    </div>

    <script>
        const dailyData = {daily_json};
        const weeklyData = {weekly_json};
        const monthlyData = {monthly_json};

        let currentChart = null;
        let currentView = 'daily';

        function showChart(view, clickEvent) {{
            currentView = view;

            // Update tabs
            document.querySelectorAll('.chart-tab').forEach(tab => {{
                tab.classList.remove('active');
            }});

            // If called from button click, update active state
            if (clickEvent && clickEvent.target) {{
                clickEvent.target.classList.add('active');
            }} else {{
                // If called programmatically, activate the corresponding tab
                document.querySelectorAll('.chart-tab').forEach(tab => {{
                    if (tab.onclick && tab.onclick.toString().includes(view)) {{
                        tab.classList.add('active');
                    }}
                }});
            }}

            let labels, data;

            if (view === 'daily') {{
                labels = dailyData.map(d => {{
                    const date = new Date(d.day);
                    return date.toLocaleDateString('en-US', {{ month: 'short', day: 'numeric' }});
                }});
                data = dailyData.map(d => d.downloads);
            }} else if (view === 'weekly') {{
                labels = weeklyData.map(d => d.label);
                data = weeklyData.map(d => d.downloads);
            }} else if (view === 'monthly') {{
                labels = monthlyData.map(d => d.label);
                data = monthlyData.map(d => d.downloads);
            }}

            if (currentChart) {{
                currentChart.destroy();
            }}

            const ctx = document.getElementById('downloadChart').getContext('2d');

            currentChart = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: 'Downloads',
                        data: data,
                        borderColor: '#1d1d1f',
                        backgroundColor: 'rgba(29, 29, 31, 0.08)',
                        borderWidth: 2.5,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 4,
                        pointHoverRadius: 7,
                        pointBackgroundColor: '#1d1d1f',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointHoverBackgroundColor: '#1d1d1f',
                        pointHoverBorderColor: '#fff',
                        pointHoverBorderWidth: 3
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {{
                        intersect: false,
                        mode: 'index'
                    }},
                    plugins: {{
                        legend: {{
                            display: false
                        }},
                        tooltip: {{
                            backgroundColor: 'rgba(29, 29, 31, 0.95)',
                            padding: 14,
                            titleColor: '#fff',
                            titleFont: {{
                                size: 13,
                                weight: '600'
                            }},
                            bodyColor: '#fff',
                            bodyFont: {{
                                size: 14
                            }},
                            borderColor: 'rgba(255, 255, 255, 0.1)',
                            borderWidth: 1,
                            cornerRadius: 8,
                            displayColors: false,
                            callbacks: {{
                                label: function(context) {{
                                    return 'Downloads: ' + context.parsed.y.toLocaleString();
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            grid: {{
                                color: 'rgba(0, 0, 0, 0.06)',
                                drawBorder: false
                            }},
                            ticks: {{
                                font: {{
                                    size: 12,
                                    family: 'Inter'
                                }},
                                color: '#6e6e73',
                                callback: function(value) {{
                                    return value.toLocaleString();
                                }}
                            }}
                        }},
                        x: {{
                            grid: {{
                                display: false,
                                drawBorder: false
                            }},
                            ticks: {{
                                font: {{
                                    size: 12,
                                    family: 'Inter'
                                }},
                                color: '#6e6e73',
                                maxRotation: 45,
                                minRotation: 0
                            }}
                        }}
                    }},
                    animation: {{
                        duration: 750,
                        easing: 'easeInOutQuart'
                    }}
                }}
            }});
        }}

        // Initialize chart on load if data is available
        window.addEventListener('load', () => {{
            if (dailyData.length > 0) {{
                showChart('daily');
            }}
        }});
    </script>
</body>
</html>"""

    return html

def main():
    if len(sys.argv) < 4:
        print("Usage: python generate_stylish_proof.py <package-name> <start-date> <end-date>")
        print("\nExample:")
        print("  python generate_stylish_proof.py mcp-server-kubernetes 2025-11-27 2025-12-03")
        print("\nThis generates a beautiful, Apple-style proof document with:")
        print("  - Clean white and light gray design")
        print("  - Smooth animations")
        print("  - Interactive charts (daily/weekly/monthly)")
        print("  - Professional appearance")
        sys.exit(1)

    package_name = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]

    print(f"Fetching download statistics for {package_name}...")
    print(f"Period: {start_date} to {end_date}\n")

    # Fetch summary data
    data = fetch_downloads(package_name, start_date, end_date)

    if not data:
        print("❌ Failed to fetch download statistics.")
        sys.exit(1)

    print(f"✓ Successfully fetched summary: {data['downloads']:,} downloads")

    # Fetch detailed range data for charts
    print("Fetching detailed data for charts...")
    range_data = fetch_range_data(package_name, start_date, end_date)

    if range_data:
        print(f"✓ Successfully fetched {len(range_data.get('downloads', []))} days of data\n")
    else:
        print("⚠ Could not fetch detailed data, proceeding without charts\n")

    # Generate HTML report
    html_content = generate_html_report(package_name, start_date, end_date, data, range_data)

    # Save to file
    output_filename = f"stylish_proof_{package_name}_{start_date}_to_{end_date}.html"
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✓ Beautiful proof document generated: {output_filename}")
    print("\nFeatures:")
    print("  - Apple-style design with clean white and gray colors")
    print("  - Interactive charts showing download trends")
    print("  - Daily, weekly, and monthly views")
    print("  - Smooth animations and modern UI")
    print("  - Fully responsive design")
    print("\nNext steps:")
    print("  1. Open the HTML file in your browser to see the beautiful design")
    print("  2. Save as PDF (File > Print > Save as PDF)")
    print("  3. Submit as proof!")

if __name__ == "__main__":
    main()
