for omega in 0.55 0.6 0.65
do
    local_target_folder="original-data-local-${omega}"
    mkdir -p $local_target_folder
    python3 ../main.py -d 5 -O $omega -m $local_target_folder -f ../data/original_data.pkl -e true
done
