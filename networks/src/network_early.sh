#!/usr/bin/env bash
# what to run
NET=true
SUM=false

# plot networks
if [ $NET = true ]
then
	python /work/china-twitter2/networks/src/network_early.py \
		-in  /work/china-twitter2/data/early_clean_nw.csv \
		-out /work/china-twitter2/networks/fig/network_early \
		-n 13
fi 

# summary stats
if [ $SUM = true ]
then
	# summary stats (diplomat/media)
	python /work/china-twitter2/networks/src/summary_stats_focus.py \
		-in  /work/china-twitter2/networks/data/early_clean_nw.csv \
		-out /work/china-twitter2/networks/fig/stats_early
fi 
