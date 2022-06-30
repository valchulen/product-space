mkdir -p full-local
mkdir -p full-global

python ../main.py -d 5 -O 0.5 -m full-local -f ../data/stage1_data.pkl -e true
python ../main.py -d 5 -O 0.5 -m full-global -u true -f ../data/stage1_data.pkl -e true
