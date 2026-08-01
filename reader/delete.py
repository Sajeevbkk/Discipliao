from db import db
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
    if not (time_id := helper.choose_time(day_id)): return

    db.delete_time(time_id)
