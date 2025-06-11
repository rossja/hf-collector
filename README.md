# HF Collector

A Python tool for downloading and collecting datasets from Hugging Face collections in bulk.

## Overview

HF Collector provides two methods for downloading datasets from Hugging Face collections:

1. **Dataset Download** (`fetch_datasets.py`) - Downloads datasets using the Hugging Face `datasets` library
2. **Git Clone** (`fetch_datasets_git.py`) - Clones dataset repositories using Git

## Features

- 🔍 **Automatic Collection Parsing** - Scrapes Hugging Face collection pages to extract dataset IDs
- 🚀 **Parallel Downloads** - Multi-threaded downloading for faster collection processing
- 📁 **Organized Storage** - Saves datasets with clean directory structures
- ⏭️ **Skip Existing** - Automatically skips already downloaded datasets
- 🔒 **Authentication Support** - Optional auth token support for private datasets

## Installation

### Prerequisites

- Python 3.13 or higher
- Git (for `fetch_datasets_git.py`)

### Using uv (recommended)

```bash
# Clone the repository
git clone https://github.com/rossja/hf-collector.git
cd hf-collector

# Install dependencies with uv
uv install
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/rossja/hf-collector.git
cd hf-collector

# Install dependencies
pip install beautifulsoup4>=4.13.4 datasets>=3.6.0 requests>=2.32.4 tqdm>=4.67.1
```

## Usage

### Method 1: Dataset Download (Recommended)

Downloads datasets using the Hugging Face `datasets` library, which handles data loading and processing automatically.

```bash
python fetch_datasets.py
```

**Features:**
- Downloads processed datasets ready for use
- Supports various dataset formats
- Handles authentication if required
- Progress bar with status updates

### Method 2: Git Clone

Clones the raw dataset repositories, giving you access to all files including metadata, README files, and raw data files.

```bash
python fetch_datasets_git.py
```

**Features:**
- Full repository history (shallow clone with `--depth 1`)
- Access to all repository files
- Faster for metadata-only needs

## Configuration

### Collection URL

Both scripts are currently configured to download from the Common Pile v0.1 collection. To use a different collection, modify the `COLLECTION_URL` variable in either script:

```python
COLLECTION_URL = "https://huggingface.co/collections/your-collection-id"
```

### Download Settings

In `fetch_datasets.py`, you can adjust:

```python
SAVE_DIR = "downloaded_datasets"  # Output directory
MAX_WORKERS = 4                   # Number of parallel downloads
USE_AUTH_TOKEN = False            # Set to True for private datasets
```

### Authentication

For private datasets, set your Hugging Face token:

```python
USE_AUTH_TOKEN = True  # In fetch_datasets.py
```

Or set the `HUGGING_FACE_HUB_TOKEN` environment variable.

## Output Structure

### Dataset Download (`fetch_datasets.py`)
```
downloaded_datasets/
├── org1__dataset1/
│   ├── dataset_info.json
│   ├── state.json
│   └── [split folders]/
└── org2__dataset2/
    ├── dataset_info.json
    ├── state.json
    └── [split folders]/
```

### Git Clone (`fetch_datasets_git.py`)
```
hf_dataset_repos/
├── org1__dataset1/
│   ├── README.md
│   ├── .gitattributes
│   └── [data files]/
└── org2__dataset2/
    ├── README.md
    ├── .gitattributes
    └── [data files]/
```

## Dependencies

- **beautifulsoup4** - HTML parsing for collection scraping
- **datasets** - Hugging Face datasets library
- **requests** - HTTP requests for web scraping
- **tqdm** - Progress bars

## Error Handling

The tools include robust error handling:

- **Network errors** - Graceful handling of connection issues
- **Missing datasets** - Continues processing other datasets if one fails
- **Permission errors** - Reports authentication issues clearly
- **Disk space** - Fails gracefully on storage issues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Check existing issues in the repository
- Create a new issue with detailed information
- Include error messages and system information 