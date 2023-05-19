import sys

def word_count(file_name):
    word_count_dict = {}
    with open(file_name, 'r', encoding='latin-1') as file:
        for line in file:
            words = line.split()
            for word in words:
                if word in word_count_dict:
                    word_count_dict[word] += 1
                else:
                    word_count_dict[word] = 1

    for word, count in word_count_dict.items():
        print(f"{word} : {count}")


file_name = sys.argv[1]
word_counts = word_count(file_name)
