positive_lines = []
negative_lines = []
positive_hashmap = {}
negative_hashmap = {}
deleted_words_positive = {}
deleted_words_negative = {}
p_wi_and_next_word_in_positive = {}
p_wi_and_next_word_in_negative = {}
lambda1 = 0.7
lambda2 = 0.15
lambda3 = 0.15
e = 0.1

with open("rt-polarity.pos", "r") as file_positive:
    all_text_positive_file = file_positive.readlines()[0:5000]
    i = 0
    while i < 5000:
        positive_lines.append(all_text_positive_file[i].split())
        positive_lines[i].insert(0, "<$>")
        positive_lines[i].insert(len(positive_lines[i]), "</$>")
        i += 1
with open("rt-polarity.neg", "r") as file_negative:
    all_text_negative_file = file_negative.readlines()[0:5000]
    i = 0
    while i < 5000:
        negative_lines.append(all_text_negative_file[i].split())
        negative_lines[i].insert(0, "<$>")
        negative_lines[i].insert(len(negative_lines[i]), "</$>")
        i += 1


def get_key(val, dictionary: dict):
    for my_key, my_value in dictionary.items():
        if val == my_value:
            return my_key


def clean_lines():
    global positive_lines, negative_lines
    tmp_list = []

    for i in positive_lines:
        for j in i:
            if j == '*' or j == '.' or j == ',' or j == '?' or j == '!' or j == ':' or j == '"' or j == '[' or j == ']':
                pass
            else:
                tmp_list.append(j)
    positive_lines = tmp_list.copy()

    tmp_list.clear()
    for i in negative_lines:
        for j in i:
            if j == '*' or j == '.' or j == ',' or j == '?' or j == '!' or j == ':' or j == '"' or j == '[' or j == ']':
                pass
            else:
                tmp_list.append(j)
    negative_lines = tmp_list.copy()


def create_both_hashmap():
    for word in positive_lines:
        if word not in positive_hashmap:
            positive_hashmap[word] = 1
        else:
            positive_hashmap[word] += 1

    for word in negative_lines:
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

    for iterator in range(number_of_maximum_values):
        # [-3] is for <$> and </$>
        tmp = positive_hashmap.copy()
        value = sorted(tmp.values())[-3]
        key = get_key(value, tmp)
        deleted_words_positive[key] = positive_hashmap.pop(key)

        tmp = negative_hashmap.copy()
        value = sorted(tmp.values())[-3]
        key = get_key(value, tmp)
        deleted_words_negative[key] = negative_hashmap.pop(key)

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


def clean_lines_after_hashmap():
    global positive_lines, negative_lines
    tmp = []
    for word in positive_lines:
        if word in positive_hashmap:
            tmp.append(word)
    positive_lines = tmp.copy()
    tmp.clear()
    for word in negative_lines:
        if word in negative_hashmap:
            tmp.append(word)
    negative_lines = tmp.copy()


def calculate_probabilities_with_lambda():
    """""
    lambda1 + lambda2 + lambda3 = 1
    0 < e < 1
    e: shows accuracy if a word not in trained dictionary. 
    """""

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


clean_lines()

input_string = input()
while input_string != "!q":
    create_both_hashmap()
    clean_both_hashmap()
    # clean the lines that have stop words or repeat lower than 2
    clean_lines_after_hashmap()

    # probability of each word in language
    p_wi_in_positive = {}
    for key in positive_hashmap:
        p_wi_in_positive[key] = positive_hashmap[key] / len(positive_lines)

    p_wi_in_negative = {}
    for key in negative_hashmap:
        p_wi_in_negative[key] = negative_hashmap[key] / len(negative_lines)

    # build bigram matrices and save bigram count of each word
    bigram_matrix_positive = {}
    bigram_matrix_negative = {}

    i = 0
    while i < len(positive_lines) - 1:
        key = str(positive_lines[i] + " " + positive_lines[i + 1])
        if key not in bigram_matrix_positive:
            bigram_matrix_positive[key] = 1
        else:
            bigram_matrix_positive[key] += 1
        i += 1

    i = 0
    while i < len(negative_lines) - 1:
        key = str(negative_lines[i] + " " + negative_lines[i + 1])
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

    # j = 0
    # for i in p_wi_and_next_word_in_positive:
    #     j += 1
    #     if j > 4:
    #         break
    #     print(i, p_wi_and_next_word_in_positive[i])

    # considering lambda
    calculate_probabilities_with_lambda()
    # print("|||||")
    # j = 0
    # for i in p_wi_and_next_word_in_positive:
    #     j += 1
    #     if j > 4:
    #         break
    #     print(i, p_wi_and_next_word_in_positive[i])

    # main function
    list_input = input_string.split()
    list_input.insert(0, "<$>")
    list_input.insert(len(list_input), "</$>")

    deleted_from_input_positive = []
    deleted_from_input_negative = []
    for i in list_input:
        if i not in positive_hashmap:
            deleted_from_input_positive.append(i)
    # clean input
    for i in deleted_from_input_positive:
        if i in list_input:
            list_input.remove(i)

    for i in list_input:
        if i not in negative_hashmap:
            deleted_from_input_negative.append(i)
    # clean input
    for i in deleted_from_input_negative:
        if i in list_input:
            list_input.remove(i)

    print(list_input)

    p_multiplication_positive = p_wi_in_positive[list_input[0]]
    i = 1
    while i < len(list_input):
        two_word = str(list_input[i - 1] + " " + list_input[i])
        if two_word in p_wi_and_next_word_in_positive:
            print("sa")
            p_multiplication_positive *= p_wi_and_next_word_in_positive[two_word]
        else:
            p_multiplication_positive *= (lambda2 * p_wi_in_positive[list_input[i]]) + (lambda3 * e)
        print(two_word, p_multiplication_positive)
        i += 1

    i = 1
    p_multiplication_negative = p_wi_in_negative[list_input[0]]
    while i < len(list_input):
        two_word = str(list_input[i - 1] + " " + list_input[i])
        if two_word in p_wi_and_next_word_in_negative:
            p_multiplication_negative *= p_wi_and_next_word_in_negative[two_word]
        else:
            p_multiplication_negative *= (lambda2 * p_wi_in_negative[list_input[i]]) + (lambda3 * e)

        i += 1
    print("|||")
    print(p_multiplication_positive)
    print(p_multiplication_negative)
    input_string = input()
