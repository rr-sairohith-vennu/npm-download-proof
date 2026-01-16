#!/usr/bin/env node

/**
 * Fetch NPM package download statistics for a specific date range
 * API: https://api.npmjs.org/downloads/point/{period}/{package}
 */

const https = require('https');

function fetchDownloads(packageName, startDate, endDate) {
  const period = `${startDate}:${endDate}`;
  const url = `https://api.npmjs.org/downloads/point/${period}/${packageName}`;

  console.log(`Fetching downloads for ${packageName} from ${startDate} to ${endDate}...`);
  console.log(`URL: ${url}\n`);

  https.get(url, (res) => {
    let data = '';

    res.on('data', (chunk) => {
      data += chunk;
    });

    res.on('end', () => {
      try {
        const result = JSON.parse(data);

        if (result.downloads !== undefined) {
          console.log('✓ Success!');
          console.log(`Package: ${result.package}`);
          console.log(`Period: ${result.start} to ${result.end}`);
          console.log(`Total Downloads: ${result.downloads.toLocaleString()}`);
        } else {
          console.log('Response:', result);
        }
      } catch (error) {
        console.error('Error parsing response:', error.message);
        console.log('Raw response:', data);
      }
    });
  }).on('error', (error) => {
    console.error('Error fetching data:', error.message);
  });
}

// Parse command line arguments
const args = process.argv.slice(2);

if (args.length < 3) {
  console.log('Usage: node fetch_npm_downloads.js <package-name> <start-date> <end-date>');
  console.log('Date format: YYYY-MM-DD');
  console.log('\nExample:');
  console.log('  node fetch_npm_downloads.js mcp-server-kubernetes 2025-11-27 2025-12-03');
  process.exit(1);
}

const [packageName, startDate, endDate] = args;
fetchDownloads(packageName, startDate, endDate);
