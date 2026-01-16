#!/usr/bin/env python3

"""
Batch generate proofs for multiple date ranges
Useful for showing growth over time or comparing different periods
"""

import sys
import os
from datetime import datetime, timedelta

def run_command(cmd):
    """Execute a shell command"""
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0

def generate_weekly_proofs(package_name, num_weeks=4):
    """Generate proofs for the last N weeks"""
    print(f"Generating proofs for last {num_weeks} weeks...\n")

    end_date = datetime.now().date()
    proofs_generated = []

    for i in range(num_weeks):
        week_end = end_date - timedelta(days=i*7)
        week_start = week_end - timedelta(days=6)

        start_str = week_start.strftime('%Y-%m-%d')
        end_str = week_end.strftime('%Y-%m-%d')

        print(f"Week {i+1}: {start_str} to {end_str}")

        # Generate HTML proof
        cmd = f"python3 generate_proof.py {package_name} {start_str} {end_str}"
        if run_command(cmd):
            html_file = f"npm_downloads_proof_{package_name}_{start_str}_to_{end_str}.html"
            proofs_generated.append(html_file)
            print(f"  ✓ Generated {html_file}")
        else:
            print(f"  ✗ Failed to generate proof")

        print()

    return proofs_generated

def generate_monthly_proofs(package_name, num_months=3):
    """Generate proofs for the last N months"""
    print(f"Generating proofs for last {num_months} months...\n")

    today = datetime.now().date()
    proofs_generated = []

    for i in range(num_months):
        # Calculate month boundaries
        if i == 0:
            # Current month so far
            month_start = datetime(today.year, today.month, 1).date()
            month_end = today
        else:
            # Previous months
            year = today.year
            month = today.month - i

            if month <= 0:
                month += 12
                year -= 1

            month_start = datetime(year, month, 1).date()

            # Get last day of month
            if month == 12:
                next_month = datetime(year + 1, 1, 1).date()
            else:
                next_month = datetime(year, month + 1, 1).date()

            month_end = next_month - timedelta(days=1)

        start_str = month_start.strftime('%Y-%m-%d')
        end_str = month_end.strftime('%Y-%m-%d')

        print(f"Month {i+1}: {start_str} to {end_str}")

        # Generate HTML proof
        cmd = f"python3 generate_proof.py {package_name} {start_str} {end_str}"
        if run_command(cmd):
            html_file = f"npm_downloads_proof_{package_name}_{start_str}_to_{end_str}.html"
            proofs_generated.append(html_file)
            print(f"  ✓ Generated {html_file}")
        else:
            print(f"  ✗ Failed to generate proof")

        print()

    return proofs_generated

def generate_custom_range_proofs(package_name, ranges):
    """Generate proofs for custom date ranges"""
    print(f"Generating proofs for {len(ranges)} custom ranges...\n")

    proofs_generated = []

    for i, (start_date, end_date, label) in enumerate(ranges, 1):
        print(f"{label}: {start_date} to {end_date}")

        # Generate HTML proof
        cmd = f"python3 generate_proof.py {package_name} {start_date} {end_date}"
        if run_command(cmd):
            html_file = f"npm_downloads_proof_{package_name}_{start_date}_to_{end_date}.html"
            proofs_generated.append(html_file)
            print(f"  ✓ Generated {html_file}")
        else:
            print(f"  ✗ Failed to generate proof")

        print()

    return proofs_generated

def main():
    if len(sys.argv) < 3:
        print("Batch Proof Generator - Generate multiple proofs at once")
        print("\nUsage:")
        print("  python batch_proof_generator.py <package-name> weekly [num-weeks]")
        print("  python batch_proof_generator.py <package-name> monthly [num-months]")
        print("  python batch_proof_generator.py <package-name> custom <start1> <end1> <start2> <end2> ...")
        print("\nExamples:")
        print("  # Generate proofs for last 4 weeks")
        print("  python batch_proof_generator.py mcp-server-kubernetes weekly 4")
        print("\n  # Generate proofs for last 3 months")
        print("  python batch_proof_generator.py mcp-server-kubernetes monthly 3")
        print("\n  # Generate proofs for custom ranges")
        print("  python batch_proof_generator.py mcp-server-kubernetes custom 2025-11-01 2025-11-30 2025-12-01 2025-12-31")
        sys.exit(1)

    package_name = sys.argv[1]
    mode = sys.argv[2].lower()

    proofs = []

    if mode == 'weekly':
        num_weeks = int(sys.argv[3]) if len(sys.argv) > 3 else 4
        proofs = generate_weekly_proofs(package_name, num_weeks)

    elif mode == 'monthly':
        num_months = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        proofs = generate_monthly_proofs(package_name, num_months)

    elif mode == 'custom':
        if len(sys.argv) < 5 or (len(sys.argv) - 3) % 2 != 0:
            print("Error: Custom mode requires pairs of start and end dates")
            sys.exit(1)

        ranges = []
        for i in range(3, len(sys.argv), 2):
            start = sys.argv[i]
            end = sys.argv[i + 1]
            ranges.append((start, end, f"Range {len(ranges) + 1}"))

        proofs = generate_custom_range_proofs(package_name, ranges)

    else:
        print(f"Error: Unknown mode '{mode}'. Use 'weekly', 'monthly', or 'custom'")
        sys.exit(1)

    print("=" * 70)
    print(f"✓ Successfully generated {len(proofs)} proof documents")
    print("=" * 70)
    print("\nGenerated files:")
    for proof in proofs:
        print(f"  - {proof}")

    print("\nNext steps:")
    print("  1. Open each HTML file in your browser")
    print("  2. Save as PDF (File > Print > Save as PDF)")
    print("  3. Submit the PDFs as proof")

if __name__ == "__main__":
    main()
