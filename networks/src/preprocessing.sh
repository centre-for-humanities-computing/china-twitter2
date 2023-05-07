#!/usr/bin/env bash

# setup 
VENVNAME=cnenv
source /work/cn-some/china-twitter/$VENVNAME/bin/activate
python -m ipykernel install --user --name $VENVNAME --display-name "$VENVNAME"

# run preprocessing 
if [ $PRE = true ]
then 
	python /work/cn-some/china-twiplomacy-2020-2022/networks/src/concat_files.py \
		-i /work/cn-some/china-twiplomacy-2020-2022/networks/data/raw/ \
		-op /work/cn-some/china-twiplomacy-2020-2022/networks/data/clean/ \
		-on df_raw.csv \
		-f False \
		-or False 
fi
