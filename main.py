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
    return text


# clean_negative = clean_and_pre_processing(all_text_negative_file)
# print(clean_negative)
all_text_positive_file = clean_text(all_text_positive_file)
all_text_negative_file = clean_text(all_text_negative_file)
print(all_text_negative_file)