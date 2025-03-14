import time


def word_stream(text: str):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.03)
