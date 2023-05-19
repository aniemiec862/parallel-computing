import sys
import time
import collections

def process_file(file_path, block_size=4096):
    with open(file_path, 'r', encoding='latin-1') as file:
        while True:
            block = file.read(block_size)
            if not block:
                break
            yield block.split()
def word_count(file_name):
    counter = collections.Counter()
    lines = process_file(file_name)
    for words in lines:
        counter.update(words)

    for word, count in counter.items():
        print(f"{word} : {count}")


experiment_id = sys.argv[1]
file_size = sys.argv[2]
file_name = "gutenberg-" + file_size + "GB.txt"
start = time.time()
word_count(file_name)
result = time.time() - start

with open('result.txt', 'a') as f:
    print(str(experiment_id) + ";" + file_size + ";" + str(result), file=f)
