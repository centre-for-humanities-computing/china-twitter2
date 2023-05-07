#!/usr/bin/env bash

# setup 
VENVNAME=cnenv
source /work/cn-some/china-twiplomacy-2020-2022/$VENVNAME/bin/activate
python -m ipykernel install --user --name $VENVNAME --display-name "$VENVNAME"

# what to run
NET=true
SUM=false

# plot networks
if [ $NET = true ]
then
	python /work/cn-some/china-twiplomacy-2020-2022/networks/src/network_early.py \
		-in  /work/cn-some/china-twiplomacy-2020-2022/networks/data/clean/early_clean.csv \
		-out /work/cn-some/china-twiplomacy-2020-2022/networks/fig/network_early \
		-n 13
fi 

# summary stats
if [ $SUM = true ]
then
	# summary stats (diplomat/media)
	python /work/cn-some/china-twiplomacy-2020-2022/networks/src/summary_stats_focus.py \
		-in  /work/cn-some/china-twiplomacy-2020-2022/networks/data/clean/early_clean.csv \
		-out /work/cn-some/china-twiplomacy-2020-2022/networks/fig/stats_early
fi 
