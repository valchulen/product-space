target_folder=metrics
duration=20
mkdir -p $target_folder

for omega in 0.1 0.2 0.3 0.4 0.5 0.55 0.6 0.65 0.8 0.9
do
    echo false $omega

    local_target_folder="${target_folder}-false-${omega}"
    mkdir -p $local_target_folder
    python ../main.py -d $duration -O $omega -m $local_target_folder -f ../data/stage1_data.pkl

    echo true $omega

    local_target_folder="${target_folder}-true-${omega}"
    mkdir -p $local_target_folder
    python ../main.py -d $duration -O $omega -m $local_target_folder -u true -f ../data/stage1_data.pkl
    
done