original_data.pkl: wtf_data/wtf98.sas7bdat wtf_data/wtf99.sas7bdat wtf_data/wtf00.sas7bdat
	python3 original_data_preprocess.py

wtf_data/wtf98.sas7bdat:
	mkdir -p wtf_data
	wget https://cid.econ.ucdavis.edu/data/undata/wtf98.zip
	unzip wtf98.zip -d wtf_data
	rm wtf98.zip

wtf_data/wtf99.sas7bdat:
	mkdir -p wtf_data
	wget https://cid.econ.ucdavis.edu/data/undata/wtf99.zip
	unzip wtf99.zip -d wtf_data
	rm wtf99.zip

wtf_data/wtf00.sas7bdat:
	mkdir -p wtf_data
	wget https://cid.econ.ucdavis.edu/data/undata/wtf00.zip
	unzip wtf00.zip -d wtf_data
	rm wtf00.zip
