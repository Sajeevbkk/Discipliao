from db import db
from datetime import time as time_obj

def choose_subject():
    print("\nChoose a Subject:")
    subjects = db.get_subjects()

    if not subjects:
        return None

    subject_ids = []
    for s_id, subject, _ in subjects:
        print(f"\t{s_id} - {subject}")
        subject_ids.append(s_id)

    try:
        subject_id = int(input("\tSelect Subject ID: "))
    except ValueError:
        print("Subject ID must be an integer!!\tOPERATION CANCELLED")
        return None

    if subject_id not in subject_ids:
        print("Subject ID is invalid!!\tOPERATION CANCELLED")
        return None

    return subject_id

def choose_chapter(subject_id):
    print("\nChoose a Chapter:")
    chapters = db.get_chapters(subject_id)

    if not chapters: return None

    chapter_ids = []
    for ch_id, chapter, _ in chapters:
        print(f"\t{ch_id} - {chapter}")
        chapter_ids.append(ch_id)

    try:
        chapter_id = int(input("\tSelect Chapter ID: "))
    except ValueError:
        print("Chapter ID must be an integer!!\tOPERATION CANCELLED")
        return None

    if chapter_id not in chapter_ids:
        print("Chapter ID is invalid!!\tOPERATION CANCELLED")
        return None

    return chapter_id

def choose_topic(chapter_id):
    print("\nChoose a Topic:")
    topics = db.get_topics(chapter_id)

    if not topics:
        print("No Topics Found")
        return None

    topic_ids = []
    for topic in topics:
        t_id, name = topic[0:2]
        print(f"\t{t_id} - {name}")
        topic_ids.append(t_id)

    try:
        topic_id = int(input("\tSelect Topic ID: "))
    except ValueError:
        print("Topic ID must be an integer!!\tOPERATION CANCELLED")
        return None

    if topic_id not in topic_ids:
        print("Topic ID is invalid!!\tOPERATION CANCELLED")
        return None

    return topic_id

def choose_day():
    print("\nChoose a day:")
    days = db.get_days()

    if not days:
        print("Add Days to Continue!!")
        return None

    day_ids = []
    for day_id, day in days:
        print(f"\t{day_id} - {day}")
        day_ids.append(day_id)

    try:
        day_id = int(input("\nEnter Day ID: "))
    except ValueError:
        print("Day ID must be an integer!!\tOPERATION CANCELLED!!")
        return None

    if day_id not in day_ids:
        print("Day ID is invalid!!\tOPERATION CANCELLED!!")
        return None

    return day_id

def choose_time(day_id):
    print("\nChoose Time:")
    times = db.get_times(day_id)

    if not times: return None

    time_ids = []
    for time in times:
        f_time = (time_obj(time[1], time[2])).strftime("%I:%M%p")
        print(f"\t{time[0]} - {f_time}")
        time_ids.append(time[0])

    try:
        time_id = int(input("\nSelect Time ID: "))
    except ValueError:
        print("Time ID must be an integer!!\tOPERATION CANCELLED")
        return None

    if time_id not in time_ids:
        print("Time ID is invalid!!\tOPERATION CANCELLED")
        return None

    return time_id

def validate_priority(priority):
    try:
        priority = int(priority)
    except ValueError:
        print("Priority must be an integer!!\tOPERATION CANCELLED")
        return None

    if not (1 <= priority <= 10):
        print("Priority must be between 1 and 10!!\tOPERATION CANCELLED!!")
        return None
    return priority