# Intento replicar grafos del paper de Hidalgo

for omega in 0.55 0.6 0.65
do
    local_target_folder="local-custom-${omega}"
    mkdir -p $local_target_folder
    python ../main.py -d 5 -O $omega -m $local_target_folder -f ../data/stage1_data_custom.pkl -e true
done
