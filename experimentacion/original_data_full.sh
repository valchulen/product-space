omega=0.55

#local_target_folder="original-data-local-${omega}"
#mkdir -p $local_target_folder
#python3 ../main.py -d 5 -O $omega -m $local_target_folder -f ../data/original_data.pkl -e true

local_target_folder="original-data-global-${omega}"
mkdir -p $local_target_folder
python3 ../main.py -d 5 -O $omega -m $local_target_folder -u true -f ../data/original_data.pkl -e true
