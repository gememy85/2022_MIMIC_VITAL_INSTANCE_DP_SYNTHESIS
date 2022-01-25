all: data/processed/death_numpy.csv\
	 data/processed/live_numpy.csv

data/processed/death_df.csv data/processed/live_df.csv: code/extract_dataframe.py
	python code/extract_dataframe.py

data/processed/death_numpy.csv data/processed/live_numpy.csv: code/dataframe_to_numpy.py \
	data/processed/death_df.csv\
	data/processed/live_df.csv	
	python code/dataframe_to_numpy.py


