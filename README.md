# NPM Package Download Statistics Tools

Tools to fetch npm package download statistics for specific date ranges using the official NPM Registry API.

## Available Scripts

### 1. Basic Download Fetcher (`fetch_npm_downloads.py`)

Fetch downloads for a single date range.

**Usage:**
```bash
python3 fetch_npm_downloads.py <package-name> <start-date> <end-date>
```

**Example:**
```bash
python3 fetch_npm_downloads.py mcp-server-kubernetes 2025-11-27 2025-12-03
```

**Output:**
```
Fetching downloads for mcp-server-kubernetes from 2025-11-27 to 2025-12-03...
✓ Success!
Package: mcp-server-kubernetes
Period: 2025-11-27 to 2025-12-03
Total Downloads: 4,419
```

### 2. Comprehensive Report (`npm_downloads_report.py`)

Generate reports with multiple date ranges (last 7 days, 30 days, year-to-date).

**Basic Usage:**
```bash
python3 npm_downloads_report.py <package-name>
```

**With Custom Date Range:**
```bash
python3 npm_downloads_report.py <package-name> <start-date> <end-date> "Custom Label"
```

**Examples:**
```bash
# Basic report
python3 npm_downloads_report.py mcp-server-kubernetes

# With custom range
python3 npm_downloads_report.py mcp-server-kubernetes 2025-11-27 2025-12-03 "Spike Week"
```

### 3. Node.js Version (`fetch_npm_downloads.js`)

JavaScript/Node.js implementation.

**Usage:**
```bash
node fetch_npm_downloads.js <package-name> <start-date> <end-date>
```

**Example:**
```bash
node fetch_npm_downloads.js mcp-server-kubernetes 2025-11-27 2025-12-03
```

## Date Format

All dates must be in `YYYY-MM-DD` format.

## NPM API Endpoints

These tools use the official NPM Registry API:
- **Endpoint:** `https://api.npmjs.org/downloads/point/{period}/{package}`
- **Period format:** `YYYY-MM-DD:YYYY-MM-DD` (start:end)
- **Documentation:** https://github.com/npm/registry/blob/master/docs/download-counts.md

## Example Use Cases

### Compare Weekly Performance
```bash
python3 fetch_npm_downloads.py mcp-server-kubernetes 2025-11-20 2025-11-26
python3 fetch_npm_downloads.py mcp-server-kubernetes 2025-11-27 2025-12-03
python3 fetch_npm_downloads.py mcp-server-kubernetes 2025-12-04 2025-12-10
```

### Track Launch Impact
```bash
# Week before launch
python3 fetch_npm_downloads.py mcp-server-kubernetes 2025-11-20 2025-11-26

# Launch week
python3 fetch_npm_downloads.py mcp-server-kubernetes 2025-11-27 2025-12-03

# Week after
python3 fetch_npm_downloads.py mcp-server-kubernetes 2025-12-04 2025-12-10
```

### Monthly Comparison
```bash
python3 fetch_npm_downloads.py mcp-server-kubernetes 2025-11-01 2025-11-30
python3 fetch_npm_downloads.py mcp-server-kubernetes 2025-12-01 2025-12-31
```

## Generating Proof Documents (NEW!)

### ✨ Stylish Proof with Interactive Charts (`generate_stylish_proof.py`) - RECOMMENDED!

Generate a beautiful, Apple-style proof document with interactive charts showing download trends.

**Usage:**
```bash
python3 generate_stylish_proof.py <package-name> <start-date> <end-date>
```

**Example:**
```bash
python3 generate_stylish_proof.py mcp-server-kubernetes 2025-11-01 2025-12-31
```

**Features:**
- 🎨 Beautiful Apple-inspired design with smooth animations
- 📊 Interactive charts with daily, weekly, and monthly views
- 🌈 Gradient backgrounds and modern UI elements
- 📱 Fully responsive design
- 🖨️ Print-optimized for perfect PDFs
- ⚡ Smooth scrolling and hover effects
- 📈 Visual representation of download trends over time

**Output:** Creates a stunning HTML file that includes:
- Hero section with gradient background and animations
- Large, prominent download statistics
- Interactive Chart.js charts showing trends
- Switchable views (daily/weekly/monthly)
- All verification information and links
- Modern card-based layout
- Professional Inter font typography

**Perfect for:**
- Investor presentations
- Grant applications
- Portfolio showcases
- Marketing materials
- Social media proof

**To Submit as PDF:**
1. Run the script to generate the HTML file
2. Open the HTML file in your web browser
3. Print the page (File > Print or Cmd/Ctrl + P)
4. Choose "Save as PDF"
5. Submit the PDF as proof

### HTML Proof Report (`generate_proof.py`)

Generate a professional, verifiable HTML report (simpler version without charts).

**Usage:**
```bash
python3 generate_proof.py <package-name> <start-date> <end-date>
```

**Example:**
```bash
python3 generate_proof.py mcp-server-kubernetes 2025-11-27 2025-12-03
```

**Output:** Creates an HTML file with:
- Official download numbers in a professional format
- Verification URL that anyone can use to confirm the data
- Timestamp of when the report was generated
- Verification hash for authenticity
- All official links (NPM package, GitHub repo, API endpoint)

### JSON Proof (`generate_json_proof.py`)

Generate a machine-readable proof document in JSON format.

**Usage:**
```bash
python3 generate_json_proof.py <package-name> <start-date> <end-date>
```

**Example:**
```bash
python3 generate_json_proof.py mcp-server-kubernetes 2025-11-27 2025-12-03
```

**Output:** Creates a JSON file containing:
- All download statistics
- Verification URL and API response
- Cryptographic signature hash
- Timestamp and metadata

**Use Cases for Proof Documents:**
- Submit to investors showing package traction
- Provide evidence for grant applications
- Document growth metrics for reports
- Verify download claims with third parties
- Include in project portfolios or case studies

## Notes

- The NPM API aggregates downloads across all versions of a package
- Data is updated daily
- Historical data is available going back several years
- There may be slight delays in data availability
- **Proof documents include verification URLs** - anyone can independently confirm the data is authentic
