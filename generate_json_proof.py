#!/usr/bin/env python3

"""
Generate JSON proof of NPM package download statistics
Creates a machine-readable proof that can be verified programmatically
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
        return None

def generate_proof(package_name, start_date, end_date, data):
    """Generate JSON proof document"""

    timestamp = datetime.now().isoformat()
    verification_url = f"https://api.npmjs.org/downloads/point/{start_date}:{end_date}/{package_name}"

    # Create signature data
    signature_data = {
        "package": package_name,
        "start_date": data['start'],
        "end_date": data['end'],
        "downloads": data['downloads'],
        "timestamp": timestamp
    }

    # Generate hash for verification
    signature_string = json.dumps(signature_data, sort_keys=True)
    signature_hash = hashlib.sha256(signature_string.encode()).hexdigest()

    proof = {
        "proof_version": "1.0",
        "generated_at": timestamp,
        "package": {
            "name": package_name,
            "npm_url": f"https://www.npmjs.com/package/{package_name}",
            "github_url": f"https://github.com/Flux159/{package_name}"
        },
        "statistics": {
            "start_date": data['start'],
            "end_date": data['end'],
            "total_downloads": data['downloads']
        },
        "verification": {
            "api_url": verification_url,
            "api_response": data,
            "signature_hash": signature_hash,
            "verification_method": "Anyone can verify by calling the API URL above"
        },
        "metadata": {
            "report_type": "npm_download_statistics_proof",
            "data_source": "Official NPM Registry API",
            "api_documentation": "https://github.com/npm/registry/blob/master/docs/download-counts.md"
        }
    }

    return proof

def main():
    if len(sys.argv) < 4:
        print("Usage: python generate_json_proof.py <package-name> <start-date> <end-date>")
        print("\nExample:")
        print("  python generate_json_proof.py mcp-server-kubernetes 2025-11-27 2025-12-03")
        sys.exit(1)

    package_name = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]

    print(f"Fetching download statistics for {package_name}...")

    data = fetch_downloads(package_name, start_date, end_date)

    if not data:
        print("❌ Failed to fetch download statistics.")
        sys.exit(1)

    print(f"✓ Successfully fetched data: {data['downloads']:,} downloads\n")

    # Generate proof
    proof = generate_proof(package_name, start_date, end_date, data)

    # Save to file
    output_filename = f"npm_downloads_proof_{package_name}_{start_date}_to_{end_date}.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(proof, f, indent=2)

    print(f"✓ JSON proof generated: {output_filename}")
    print(f"\nProof Details:")
    print(f"  Package: {package_name}")
    print(f"  Period: {start_date} to {end_date}")
    print(f"  Downloads: {data['downloads']:,}")
    print(f"  Signature Hash: {proof['verification']['signature_hash'][:32]}...")
    print(f"\nVerification URL:")
    print(f"  {proof['verification']['api_url']}")

if __name__ == "__main__":
    main()
