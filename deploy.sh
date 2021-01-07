#!/bin/bash

app_target="eurphon@eurphon.info:eurphon"
static_target="root@eurphon.info:/var/www/"
search_eurphon="search"
search_phoible="phoible"

rsync *.json $app_target
rsync *.py $app_target
rsync comparisonquery $app_target
rsync countquery $app_target
rsync phonemequery $app_target

rsync -r webapp/search/* "$static_target$search_eurphon"
rsync -r webapp/search_phoible/* "$static_target$search_phoible"
