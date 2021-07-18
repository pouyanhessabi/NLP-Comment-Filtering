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


all_text_positive_file = clean_text(all_text_positive_file)
all_text_negative_file = clean_text(all_text_negative_file)

positive_lines = all_text_positive_file.splitlines()
negative_lines = all_text_negative_file.splitlines()

create_both_hashmap()
