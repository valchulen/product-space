# Intento replicar grafos del paper de Hidalgo

for omega in 0.55 0.6 0.65
do
    local_target_folder="local-${omega}"
    mkdir -p $local_target_folder
    python3 ../main.py -d 5 -O $omega -m $local_target_folder -f ../data/stage1_data_custom.pkl -e true
done
