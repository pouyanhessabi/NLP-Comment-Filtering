positive_hashmap = {}
negative_hashmap = {}
positive_lines = []
negative_lines = []
deleted_words_positive = {}
deleted_words_negative = {}
positive_lines_word_by_word = []
negative_lines_word_by_word = []
p_wi_and_next_word_in_positive = {}
p_wi_and_next_word_in_negative = {}

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
    text = text.replace('"', '')
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


def update_and_clean_lines():
    for i in deleted_words_positive:
        count = positive_lines_word_by_word.count(i)
        for j in range(count):
            positive_lines_word_by_word.remove(i)

    for i in deleted_words_negative:
        count = negative_lines_word_by_word.count(i)
        for j in range(count):
            negative_lines_word_by_word.remove(i)


def calculate_probabilities_with_lambda():
    """""
    lambda1 + lambda2 + lambda3 = 1
    0 < e < 1
    e: shows accuracy if a word not in trained dictionary. 
    """""
    lambda1 = 0.15
    lambda2 = 0.7
    lambda3 = 0.15
    e = 0.1
    for key in bigram_matrix_positive:
        if (key.split()[0] in positive_hashmap) and (key.split()[0] not in deleted_words_positive) and \
                (key.split()[1] not in deleted_words_positive):
            p_wi_and_next_word_in_positive[key] = (lambda3 * p_wi_and_next_word_in_positive[key]) + \
                                                  (lambda2 * p_wi_in_positive[key.split()[0]]) + (lambda1 * e)

    for key in bigram_matrix_negative:
        if (key.split()[0] in negative_hashmap) and (key.split()[0] not in deleted_words_negative) and \
                (key.split()[1] not in deleted_words_negative):
            p_wi_and_next_word_in_negative[key] = (lambda3 * p_wi_and_next_word_in_negative[key]) + \
                                                  (lambda2 * p_wi_in_negative[key.split()[0]]) + (lambda1 * e)


all_text_positive_file = clean_text(all_text_positive_file)
all_text_negative_file = clean_text(all_text_negative_file)

positive_lines = all_text_positive_file.splitlines()
negative_lines = all_text_negative_file.splitlines()

create_both_hashmap()
clean_both_hashmap()

# add <$> at the first of line and </$> at the end of line
i = 0
while i < len(positive_lines):
    positive_lines[i] = "<$> " + positive_lines[i] + " </$>"
    i += 1
# add to hashmap
positive_hashmap["<$>"] = i
positive_hashmap["</$>"] = i

i = 0
while i < len(negative_lines):
    negative_lines[i] = "<$> " + negative_lines[i] + " </$>"
    i += 1
# add to hashmap
negative_hashmap["<$>"] = i
negative_hashmap["</$>"] = i

# probability of each word in language
p_wi_in_positive = {}
number_of_words_positive = sum(positive_hashmap.values())
for key in positive_hashmap:
    p_wi_in_positive[key] = positive_hashmap[key] / number_of_words_positive

p_wi_in_negative = {}
number_of_words_negative = sum(negative_hashmap.values())
for key in negative_hashmap:
    p_wi_in_negative[key] = negative_hashmap[key] / number_of_words_negative

positive_lines_word_by_word = str(positive_lines).split()
negative_lines_word_by_word = str(negative_lines).split()

# make it clean with stop words
# update_and_clean_lines()

# build bigram matrices and save bigram count of each word
bigram_matrix_positive = {}
bigram_matrix_negative = {}

i = 0
while i < len(positive_lines_word_by_word) - 1:
    key = str(positive_lines_word_by_word[i] + " " + positive_lines_word_by_word[i + 1] + " ")
    if key not in bigram_matrix_positive:
        bigram_matrix_positive[key] = 1
    else:
        bigram_matrix_positive[key] += 1
    i += 1

i = 0
while i < len(negative_lines_word_by_word) - 1:
    key = str(negative_lines_word_by_word[i] + " " + negative_lines_word_by_word[i + 1] + " ")
    if key not in bigram_matrix_negative:
        bigram_matrix_negative[key] = 1
    else:
        bigram_matrix_negative[key] += 1
    i += 1

# calculate probability of p(wi|w<i-1>)
for key in bigram_matrix_positive:
    if (key.split()[0] in positive_hashmap) and (key.split()[0] not in deleted_words_positive) and \
            (key.split()[1] not in deleted_words_positive):
        p_wi_and_next_word_in_positive[key] = bigram_matrix_positive[key] / positive_hashmap[key.split()[0]]
for key in bigram_matrix_negative:
    if (key.split()[0] in negative_hashmap) and (key.split()[0] not in deleted_words_negative) and \
            (key.split()[1] not in deleted_words_negative):
        p_wi_and_next_word_in_negative[key] = bigram_matrix_negative[key] / negative_hashmap[key.split()[0]]

# considering lambda
calculate_probabilities_with_lambda()
print("calculate probabilities fixed bugs")