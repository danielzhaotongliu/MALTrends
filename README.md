# MALTrends

This is a web scraper for MyAnimeList score progressions on the Wayback Machine internet archive.

The data gathered from this repo is used in another project [MALTrendsWeb](https://github.com/danielzhaotongliu/MALTrendsWeb/)
 
## Installation

### Prerequisites

- Make sure you have a version of `python3` and `virtualenv` installed.  
See `https://virtualenv.pypa.io/en/latest/installation/` for installation instructions.

### Clone

- Clone this repo to your local machine using `https://github.com/danielzhaotongliu/MALTrends`

### First Time Setup

- Navigate to the MALTrends root directory, then run the following commands to setup virtualenv and install libraries

```shell
$ virtualenv -p python3 venv/
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Usage

### Running the Project

```shell
$ source venv/bin/activate
```

### Scrape Anime Statistics

- Before running the spiders you need the MyAnimeList anime ID for the anime that you would like to scrape for

> For example: the anime ID for Sword Art Online is 11757

- Run the following command in the MALTrends root directory

```shell
$ scrapy crawl score_spider -a id=mal_id -o snapshots_mal_id.jl
```

### Generate Interactive Time Series Graph

```shell
$ python plot.py
```