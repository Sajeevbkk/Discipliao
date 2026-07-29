from reader import helper
from db import db
from random import choices

def process_input():
    if not (day_id := helper.choose_day()): return

    create_table(day_id)

def create_table(day_id):
    if not (times := db.get_times(day_id)): return
    if not (topics := db.get_active_topics()): return

    selected_topics = choices(topics,
            [topic[5] + db.get_subject_priority(topic[0]) for topic in topics],
            k = len(times))

    print("Time Table")
    for time, topic in zip(times, selected_topics):
        print(time, topic)