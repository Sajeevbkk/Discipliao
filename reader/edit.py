from db import db
from reader import helper
from datetime import time as time_obj, datetime

def edit_input():
    print("\nChoose an option:")
    print("\t1 - Edit Subject")
    print("\t2 - Edit Chapter")
    print("\t3 - Edit Topic")
    print("\t4 - Edit Day")
    print("\t5 - Edit Timing")

    try:
        option = int(input(" : "))
    except ValueError:
        print("Please enter a number!!\tOPERATION CANCELLED!!")
        return

    match option:
        case 1:
            edit_subject()
        case 2:
            edit_chapter()
        case 3:
            edit_topic()
        case 4:
            edit_day()
        case 5:
            edit_timing()
        case _:
            print("Invalid option!!\tOPERATION CANCELLED!!")

def edit_subject():
    # Choosing subject
    if not (subject_id := helper.choose_subject()): return

    subject = db.get_subject(subject_id)

    name = input(f"Enter New Name for Subject (Old Name: {subject[1]}): ")

    if not (
            priority := helper.validate_priority(
                input(f"Enter Priority (Old Priority: {subject[2]}): ")
            )
    ): return

    db.edit_subject(subject_id, name, priority)

def edit_chapter():
    # Choosing subject
    if not (subject_id := helper.choose_subject()): return

    # Choosing chapter
    if not (chapter_id := helper.choose_chapter(subject_id)): return

    chapter = db.get_chapter(chapter_id)

    name = input(f"Enter New Name for Chapter (Old Name: {chapter[1]}): ")

    db.edit_chapter(chapter_id, name)

def edit_topic():
    if not (subject_id := helper.choose_subject()): return
    if not (chapter_id := helper.choose_chapter(subject_id)): return
    if not (topic_id := helper.choose_topic(chapter_id)): return

    topic = db.get_topic(topic_id)

    name = input(f"Enter New Name for Topic (Old Name: {topic[1]}): ")

    currently_studying = input(
        f"\nAre you currently studying this topic (Old Status: {"y" if topic[3] else "n"})? (Y/N): "
    )
    if currently_studying.lower() == "y":
        currently_studying = True
    else:
        print("Considering that as an NO")
        currently_studying = False

    completed = input(f"\nDo you want to complete this topic (Old Status: {"y" if topic[4] else "n"})? (Y/N): ")
    if completed.lower() == "y":
        completed = True
    else:
        print("Considering that as an NO")
        completed = False

    if not (
            priority := helper.validate_priority(
                input(f"Enter Priority (Old Priority: {topic[5]}): ")
            )
    ): return

    db.edit_topic(topic_id, name, chapter_id, currently_studying, completed, priority)

def edit_day():
    if not (day_id := helper.choose_day()): return

    day = db.get_day(day_id)

    name = input(f"Enter New Name for Day (Old Name: {day[1]}): ")

    db.edit_day(day_id, name)

def edit_timing():
    if not (day_id := helper.choose_day()): return
    if not (time_id := helper.choose_time(day_id)): return

    time = db.get_time(time_id)

    from_time = input(f"\nEnter time (Old time: {(time_obj(time[1], time[2])).strftime("%I:%M%p")}): ")

    try:
        from_time = (datetime.strptime(from_time, "%I:%M%p"))
    except ValueError:
        print("You must use this format -> 2:36pm\tOPERATION CANCELLED!!")
        return

    db.edit_time(time_id, from_time.hour, from_time.minute)

