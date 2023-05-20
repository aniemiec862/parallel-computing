for size in 1 5 10
do
    CMD="time hadoop jar /usr/lib/hadoop/hadoop-streaming.jar -files mapper.py,reducer.py -mapper mapper.py -reducer reducer.py -input s3://aniemiec-bucket/gutenberg-{$size}GB.txt -output wordcount-output"
    for i in {1..5}
    do
        echo "Running test $i for size $size"
        ts=$(date +%s%N) ; $CMD ; tt=$((($(date +%s%N) - $ts)/1000000000)) ; echo "32;8*4;$size;$tt" >> result.txt
        hdfs dfs -rm -r wordcount-output
    done;
done;
