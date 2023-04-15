rm results.csv

values=10000000,50000000,100000000

for val in ${values//,/ }
do
    for threads in {1..4}
    do
        ./rand_numbers $threads $val >> results.csv
    done
done
