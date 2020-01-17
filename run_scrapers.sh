#!/bin/bash

while read mal_id; do
  scrapy crawl score_spider -a id=$mal_id -o snapshots_$mal_id.jl
done <mal_ids.txt