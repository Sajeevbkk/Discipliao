from db import db
from datetime import time as time_obj
from reader import helper

def delete_input():
    print("\nChoose an option:")
    print("\t1 - Delete a Subject")
    print("\t2 - Delete a Chapter")
    print("\t3 - Delete a Topic")
    print("\t4 - Delete a Day")
    print("\t5 - Delete a Timing")

    try:
        option = int(input(" : "))
    except ValueError:
        print("Please enter a number!!\tOPERATION CANCELLED!!")
        return

    match option:
        case 1:
            delete_subject()
        case 2:
            delete_chapter()
        case 3:
            delete_topic()
        case 4:
            delete_day()
        case 5:
            delete_time()
        case _:
            print("Invalid option!!\tOPERATION CANCELLED!!")

def delete_subject():
    # Choosing subject
    if not (subject_id := helper.choose_subject()): return
    db.delete_subject(subject_id)

def delete_chapter():
    # Choosing subject
    if not (subject_id := helper.choose_subject()): return

    # Choosing chapter
    if not (chapter_id := helper.choose_chapter(subject_id)): return

    db.delete_chapter(chapter_id)

def delete_topic():
    # Choosing subject
    if not (subject_id := helper.choose_subject()): return

    # Choosing chapter
    if not (chapter_id := helper.choose_chapter(subject_id)): return

    # Choosing topic
    if not (topic_id := helper.choose_topic(chapter_id)): return

    print("\nDeleting selected topic...")
    db.delete_topic(topic_id)

def delete_day():
    # Choosing Day
    if not (day_id := helper.choose_day()): return
    db.delete_day(day_id)

def delete_time():
    # Choosing Day
    if not (day_id := helper.choose_day()): return

    # Choosing Timing
    times = db.get_times(day_id)
    if not times:
        print("Add Times to Continue!!")
        return

    times_ids = []
    print("\nTimes:")
    for time in times:
        # 0 - id, 1 - hour, 2 - minute
        f_time = (time_obj(time[1], time[2])).strftime("%I:%M%p")
        print(f"\t{time[0]} - {f_time}")
        times_ids.append(time[0])

    try:
        time_id = int(input("\nEnter Time ID: "))
    except ValueError:
        print("Time ID must be an integer!!\tOPERATION CANCELLED!!")
        return

    if time_id not in times_ids:
        print("Topic ID is invalid!!\tOPERATION CANCELLED!!")
        return

    db.delete_time(time_id)
