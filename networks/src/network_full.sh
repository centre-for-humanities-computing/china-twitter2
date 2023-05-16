#!/usr/bin/env bash

# what to run
NET=true
SUM=false

# plot networks
if [ $NET = true ]
then
	python /work/china-twitter2/networks/src/network_full.py \
		-in  /work/china-twitter2/data/full_clean_nw.csv \
		-out /work/china-twitter2/networks/fig/network_full \
		-n 13
fi 

# summary stats
if [ $SUM = true ]
then
	# summary stats (diplomat/media)
	python /work/cn-some/china-twiplomacy-2020-2022/networks/src/summary_stats_focus.py \
		-in  /work/china-twitter2/data/full_clean_nw.csv \
		-out /work/china-twitter2/networks/fig/stats_full
fi 
