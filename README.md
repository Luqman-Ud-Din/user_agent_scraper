# user_agent_scraper

Scrapy-based spiders for collecting browser user-agent data from WhatIsMyBrowser developer pages.

## Overview

This repository contains a small Scrapy project that crawls user-agent listing pages and extracts structured metadata for each user agent, including:

- user-agent string
- operating system
- software name
- layout engine
- software type
- software version
- hardware type
- popularity
- source URL

The project includes:

- a crawl spider for traversing listing and pagination pages
- a parse spider for extracting structured fields from detail pages
- middleware for random user-agent rotation
- optional proxy middleware support

## Repository structure

```text
.
├── requirements.txt
├── scrapy.cfg
└── user_agents/
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders/
        └── whatismybrowser.py
```

## Requirements

- Python 3
- Scrapy 2.7.1
- python-slugify 7.0.0

Install dependencies:

```bash
pip install -r requirements.txt
```

## Getting started

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Run a spider from the repository root.

Example:

```bash
git clone <your-fork-or-repo-url>
cd user_agent_scraper
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Available spiders

### `whatismybrowser-crawl`

Starts from the WhatIsMyBrowser explore page, follows listing and pagination links, visits user-agent detail pages, and yields structured records.

Run it with:

```bash
scrapy crawl whatismybrowser-crawl
```

Export results to JSON:

```bash
scrapy crawl whatismybrowser-crawl -O user_agents.json
```

Export results to CSV:

```bash
scrapy crawl whatismybrowser-crawl -O user_agents.csv
```

### `whatismybrowser-parse`

The parse spider contains the extraction logic for a single detail page and is used internally by the crawl spider.

## Output fields

Each scraped record may contain:

- `source_url`
- `user_agent`
- `operating_system`
- `software_name`
- `software_engine`
- `software_type`
- `software_version`
- `hardware_type`
- `popularity`

## Configuration

### Random user agents

The project rotates request headers using the `USER_AGENTS` list in `user_agents/settings.py`.

### Proxies

Proxy support is available through `AutoProxyMiddleware`.

To use proxies, populate the `proxies` list in `user_agents/settings.py` with proxy URLs, for example:

```python
proxies = [
    "http://host:port",
    "http://username:password@host:port",
]
```

## Notes

- `ROBOTSTXT_OBEY` is currently set to `False` in `user_agents/settings.py`.
- The repository description says "scrap sites listing user agents"; in README text, "scrape" is used instead.
- The spider relies on the structure of the WhatIsMyBrowser developer pages, so selector updates may be needed if the site changes.

## Development suggestions

Potential improvements for the project:

- define a concrete Scrapy item in `items.py`
- enable and implement an item pipeline for validation or storage
- add tests for extraction helpers and selectors
- document supported Python versions explicitly
- add sample output for easier verification

## Contributing

Contributions are welcome. If you plan to make substantial changes, consider opening an issue first to discuss the proposed update.

## License

No license file is currently present in this repository. If you intend others to reuse the code, consider adding an open-source license.
