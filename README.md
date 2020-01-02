# MALTrends

This is a project that displays statistics over time of any anime on MyAnimeList using the Wayback Machine

## Installation

### Clone

- Clone this repo to your local machine using `https://github.com/danielzhaotongliu/MALTrends`

### First Time Setup

- Navigate to the MALTrends root directory, then run the Makefile to setup virtualenv and install libraries

```shell
$ make venv
$ make install
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
$ scrapy crawl score_spider -a id=MAL_id -o snapshots_MAL_id.jl
```

### Generate Interactive Time Series Graph

```shell
$ python plot.py
```