for size in 1 5 10
do
    ./get_data.sh $size
    for i in {1..10}
    do
        echo "Running test $i for size $size"
        python3 seq_word_count.py $i $size
    done;
    rm "gutenberg-${size}GB.txt"
done;
