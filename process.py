import random

def select_top_topics(subjects, chapters, topics, count=10):
    pool = []
    weights = []

    for topic in topics:
        if topic[3]: # truthiness of currently_studying
            chapter = None
            for chapter in chapters:
                if topic[2] == chapter[0]:
                    chapter = chapter
                    break
            print(chapter)