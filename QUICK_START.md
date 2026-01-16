# Quick Start Guide - NPM Download Proof Generator

## For Your Friend's Package: mcp-server-kubernetes

### Generate a Stylish Proof Document (RECOMMENDED!)

**Apple-style design with interactive charts:**

```bash
python3 generate_stylish_proof.py mcp-server-kubernetes 2025-11-27 2025-12-03
```

This creates: `stylish_proof_mcp-server-kubernetes_2025-11-27_to_2025-12-03.html`

**Features:**
- ✨ Beautiful Apple-style design
- 📊 Interactive charts (daily/weekly/monthly views)
- 🎨 Smooth animations and gradient backgrounds
- 📱 Fully responsive and modern UI
- 🖨️ Print-optimized for PDF export

**Then:**
1. Open the HTML file in your browser
2. Press Cmd+P (Mac) or Ctrl+P (Windows)
3. Choose "Save as PDF"
4. Submit the PDF as proof!

### Generate a Simple Proof Document

**Basic professional format:**

```bash
python3 generate_proof.py mcp-server-kubernetes 2025-11-27 2025-12-03
```

This creates: `npm_downloads_proof_mcp-server-kubernetes_2025-11-27_to_2025-12-03.html`

### Example: The Date Range From Your Screenshot

The screenshot showed **4,419 downloads** from Nov 27 to Dec 3, 2025.

```bash
python3 generate_proof.py mcp-server-kubernetes 2025-11-27 2025-12-03
```

**Output:** Professional HTML report with:
- ✓ Large display of download count (4,419)
- ✓ Official NPM API verification URL
- ✓ Timestamp of report generation
- ✓ Verification hash
- ✓ Links to package, GitHub, and API

### Generate Multiple Proofs at Once

**Last 4 weeks:**
```bash
python3 batch_proof_generator.py mcp-server-kubernetes weekly 4
```

**Last 3 months:**
```bash
python3 batch_proof_generator.py mcp-server-kubernetes monthly 3
```

**Custom date ranges:**
```bash
python3 batch_proof_generator.py mcp-server-kubernetes custom 2025-11-01 2025-11-30 2025-12-01 2025-12-31
```

### Why This Works as Proof

1. **Official Data Source**: Uses NPM's official API
2. **Verifiable**: Anyone can check the verification URL to confirm
3. **Timestamped**: Shows when the report was generated
4. **Professional Format**: Looks legitimate for submissions
5. **Signed**: Includes cryptographic hash for authenticity

### Common Use Cases

**For Investors:**
```bash
# Show growth over last 3 months
python3 batch_proof_generator.py mcp-server-kubernetes monthly 3
```

**For Grant Applications:**
```bash
# Show specific achievement period
python3 generate_proof.py mcp-server-kubernetes 2025-11-01 2025-12-31
```

**For Project Reports:**
```bash
# Year-to-date statistics
python3 generate_proof.py mcp-server-kubernetes 2026-01-01 2026-01-15
```

### Files in This Project

| File | Purpose |
|------|---------|
| `generate_stylish_proof.py` | **✨ BEST** - Apple-style design with charts |
| `generate_proof.py` | Creates professional HTML proofs |
| `batch_proof_generator.py` | Generate multiple proofs at once |
| `generate_json_proof.py` | Machine-readable JSON proof |
| `fetch_npm_downloads.py` | Simple CLI to check downloads |
| `npm_downloads_report.py` | Comprehensive report generator |
| `README.md` | Full documentation |

### Quick Commands Reference

```bash
# ✨ Stylish proof with charts (BEST for submissions!)
python3 generate_stylish_proof.py mcp-server-kubernetes 2025-11-27 2025-12-03

# Simple professional proof
python3 generate_proof.py mcp-server-kubernetes 2025-11-27 2025-12-03

# Just check the numbers
python3 fetch_npm_downloads.py mcp-server-kubernetes 2025-11-27 2025-12-03

# Multiple weeks for comparison
python3 batch_proof_generator.py mcp-server-kubernetes weekly 4

# JSON format (for APIs or automation)
python3 generate_json_proof.py mcp-server-kubernetes 2025-11-27 2025-12-03
```

### Verification URLs

The API endpoint format is:
```
https://api.npmjs.org/downloads/point/START-DATE:END-DATE/PACKAGE-NAME
```

Example:
```
https://api.npmjs.org/downloads/point/2025-11-27:2025-12-03/mcp-server-kubernetes
```

Anyone can visit this URL to verify the download count!

### Tips

1. **For submissions**: Use `generate_proof.py` - it creates the most professional looking document
2. **For multiple periods**: Use `batch_proof_generator.py` to save time
3. **For automation**: Use `generate_json_proof.py` for programmatic access
4. **Date format**: Always use YYYY-MM-DD format

### Example Real Output

When you run the proof generator, you get:

```
Fetching download statistics for mcp-server-kubernetes...
Period: 2025-11-27 to 2025-12-03

✓ Successfully fetched data: 4,419 downloads

✓ Proof document generated: npm_downloads_proof_mcp-server-kubernetes_2025-11-27_to_2025-12-03.html

Next steps:
  1. Open the HTML file in your web browser
  2. Save as PDF (File > Print > Save as PDF)
  3. Submit the PDF as proof of download statistics
```

The HTML file contains a beautiful, professional report that looks like an official document!
