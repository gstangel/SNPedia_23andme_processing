# SNPedia_23andme_processing

A Python tool for analyzing 23andMe raw genetic data using SNPedia information.

## Overview

This tool processes raw genetic data files from 23andMe and cross-references them with information from SNPedia to provide insights about genetic variants. It helps users understand their genetic variants and their potential significance based on information available in SNPedia's knowledge base.

## Features

- Parses 23andMe raw data files
- Retrieves relevant information from SNPedia
- Caches SNPedia data locally to reduce API load
- Identifies SNPs of interest based on their significance
- Provides magnitude scores for variants according to SNPedia's scale
- Generates summary reports of significant genetic variants

## Requirements

- Python 3.6+
- Required Python packages:
  - requests
  - wikitextparser
  - pandas

## Installation

Clone this repository:

```bash
git clone https://github.com/gstangel/SNPedia_23andme_processing.git
cd SNPedia_23andme_processing
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

To analyze a 23andMe raw data file:

```bash
python process_genome.py path/to/your_genome_file.txt
```

This will generate a report file in the `output` directory.

### Advanced Options

```bash
python process_genome.py --input path/to/your_genome_file.txt --output custom_output.html --cache-dir ./cache --magnitude 3
```

Parameters:
- `--input`: Path to your 23andMe raw data file
- `--output`: Path for the generated report (default: `output/report_{timestamp}.html`)
- `--cache-dir`: Directory to store cached SNPedia data (default: `./cache`)
- `--magnitude`: Minimum magnitude threshold for reporting variants (default: 2)

## Understanding the Results

The report contains information about your genetic variants organized by their "magnitude" - a score assigned by SNPedia to indicate potential significance. Higher magnitude scores generally indicate more significant variants.

For each variant, the report provides:
- The SNP identifier (rsid)
- Your genotype
- The magnitude score
- A summary of the significance
- Links to more information on SNPedia

## Limitations

- This tool relies on SNPedia's data, which may be incomplete or subject to change
- The information provided is for educational purposes only and should not be used for medical decisions
- Processing large datasets may take time, especially during the first run when caching data

## Privacy Notice

This tool processes your genetic data locally on your machine. No genetic data is transmitted to external servers except when querying the SNPedia API for specific SNPs. Only the SNP identifiers are sent in these queries, not your personal genotypes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- SNPedia for providing a valuable resource for genetic information
- The 23andMe platform for making raw genetic data accessible to users
