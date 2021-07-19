positive_hashmap = {}
negative_hashmap = {}
positive_lines = []
negative_lines = []

with open("rt-polarity.pos", "r") as file_positive:
    all_text_positive_file = file_positive.read()
with open("rt-polarity.neg", "r") as file_negative:
    all_text_negative_file = file_negative.read()


def clean_text(text: str):
    text = text.replace('*', '')
    text = text.replace('.', '')
    text = text.replace(',', '')
    text = text.replace('?', '')
    text = text.replace('!', '')
    text = text.replace(':', '')
    text = text.replace('[', '')
    text = text.replace(']', '')
    text = text.replace('-', " ")
    text = text.replace("  ", " ")
    return text


def create_both_hashmap():
    for line in positive_lines:
        for word in line.split():
            if word not in positive_hashmap:
                positive_hashmap[word] = 1
            else:
                positive_hashmap[word] += 1

    for line in negative_lines:
        for word in line.split():
            if word not in negative_hashmap:
                negative_hashmap[word] = 1
            else:
                negative_hashmap[word] += 1


def clean_both_hashmap():
    """""
    This method clean both hashmap, first delete 10(number_of_maximum_values) words with highest value(counting) then
    delete the words that repeat lower than 2(number_of_maximum_values) times
    """""
    number_of_maximum_values = 10
    number_of_minimum_values = 2
    deleted_words_positive = {}
    deleted_words_negative = {}

    # save begin and end of file

    for iterator in range(number_of_maximum_values):
        key = max(positive_hashmap, key=positive_hashmap.get)
        deleted_words_positive[key] = positive_hashmap.pop(key)

        key = max(negative_hashmap, key=negative_hashmap.get)
        deleted_words_negative[key] = negative_hashmap.pop(key)

    # print("length of positive_hashmap before cleaning:", len(positive_hashmap))
    # print("length of negative_hashmap before cleaning:", len(negative_hashmap))

    for key in positive_hashmap:
        if positive_hashmap[key] < number_of_minimum_values:
            deleted_words_positive[key] = positive_hashmap[key]
    for key in deleted_words_positive:
        if key in positive_hashmap:
            positive_hashmap.pop(key)

    for key in negative_hashmap:
        if negative_hashmap[key] < number_of_minimum_values:
            deleted_words_negative[key] = negative_hashmap[key]
    for key in deleted_words_negative:
        if key in negative_hashmap:
            negative_hashmap.pop(key)

    """""
    print("length of positive_hashmap after  cleaning:", len(positive_hashmap))
    print("length of negative_hashmap after  cleaning:", len(negative_hashmap))
    
    print(deleted_words_positive)
    print(deleted_words_negative)
    """""
    # print(deleted_words_positive)
    print(deleted_words_negative)


all_text_positive_file = clean_text(all_text_positive_file)
all_text_negative_file = clean_text(all_text_negative_file)

positive_lines = all_text_positive_file.splitlines()
negative_lines = all_text_negative_file.splitlines()

# print(positive_lines)


create_both_hashmap()
clean_both_hashmap()

# add <$> at the first of line and </$> at the end of line
i = 0
while i < len(positive_lines):
    positive_lines[i] = "<$> " + positive_lines[i] + " </$>"
    i += 1
# add to hashmaps
positive_hashmap["<$>"] = i
positive_hashmap["</$>"] = i


i = 0
while i < len(negative_lines):
    negative_lines[i] = "<$> " + negative_lines[i] + " </$>"
    i += 1
# add to hashmaps
negative_hashmap["<$>"] = i
negative_hashmap["</$>"] = i

p_in_positive = {}
all_word_from_positive = sum(positive_hashmap.values())
for key in positive_hashmap:
    p_in_positive[key] = positive_hashmap[key] / all_word_from_positive

p_in_negative = {}
all_word_from_negative = sum(negative_hashmap.values())
for key in negative_hashmap:
    p_in_negative[key] = negative_hashmap[key] / all_word_from_negative

bigram_matrix_positive = []
