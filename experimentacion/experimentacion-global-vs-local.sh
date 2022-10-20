target_folder="metrics-original-data"
#data_file="../data/stage1_data.pkl"
data_file="../data/original_data.pkl"
duration=20

for omega in 0.1 0.2 0.3 0.4 0.5 0.55 0.6 0.65 0.8 0.9
do
    echo false $omega

    local_target_folder="${target_folder}-false-${omega}"
    mkdir -p $local_target_folder
    python ../main.py -d $duration -O $omega -m $local_target_folder -f $data_file

    echo true $omega

    local_target_folder="${target_folder}-true-${omega}"
    mkdir -p $local_target_folder
    python ../main.py -d $duration -O $omega -m $local_target_folder -u true -f $data_file
    
done