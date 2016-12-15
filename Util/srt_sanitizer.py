# -*- coding: utf-8 -*-
import pysrt
import re


def open_doc(source_text):
    try:
        subs = pysrt.open(source_text)
        return subs
    except UnicodeDecodeError:
        subs = pysrt.open(source_text, encoding='iso-8859-1')
        return subs


def sanitize(subs):
    sanitized = ""

    for sub in subs:
        sanitized += sub.text + "\n"

    return sanitized


def concatinate_string_to_file(str, file):
    with open(file, "a") as corpus:
        corpus.write(str)


def orginize_sentence_end(file):
    with open(file, "r") as corpus:
        data = str(corpus.read())
        return (data.replace("\n", " ")
                .replace("? ", "?\n")
                .replace("! ", "!\n")
                .replace("...", "")
                .replace(". ", ".\n"))


def update_sanitized_corpus(the_file, text):
    with open(the_file, "w") as sanitized_corpus:
        sanitized_corpus.write(text)


# subs = open_doc("Reservoir Dogs.srt")
# sanitized_subs = sanitize(subs)
# print(tokenize_and_clean_subs(sanitized_subs))

update_sanitized_corpus("sanitized_corpus.txt",
                        orginize_sentence_end("corpus.txt"))
