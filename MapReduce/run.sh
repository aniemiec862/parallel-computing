CMD="hadoop jar /usr/lib/hadoop/hadoop-streaming.jar -files mapper.py,reducer.py -mapper mapper.py -reducer reducer.py -input words -output wordcount-output"
for size in 1 5 10
do
    ./get_data.sh $size
    for i in {1..5}
    do
        echo "Running test $i for size $size"
        ts=$(date +%s%N) ; $CMD ; tt=$((($(date +%s%N) - $ts)/1000000000)) ; echo "32;8*4;$size;$tt" >> result.txt
        hdfs dfs -rm -r wordcount-output
    done;
done;
