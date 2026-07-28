from db import db
from datetime import datetime
from reader import helper

def add_input():
    print("\nChoose an option:")
    print("\t1 - Add New Subject")
    print("\t2 - Add New Chapter")
    print("\t3 - Add New Topic")
    print("\t4 - Add New Day")
    print("\t5 - Add New Timing")

    try:
        option = int(input(" : "))
    except ValueError:
        print("Please enter a number!!\tOPERATION CANCELLED!!")
        return

    match option:
        case 1:
            add_new_subject()
        case 2:
            add_new_chapter()
        case 3:
            add_new_topic()
        case 4:
            add_new_day()
        case 5:
            add_new_timing()
        case _:
            print("Invalid option!!\tOPERATION CANCELLED!!")

def add_new_subject():
    subject = input("\nEnter Subject Name: ")
    try:
        priority = int(input("Enter Priority (1 - 10): "))
    except ValueError:
        print("Priority must be an integer!!\tOPERATION CANCELLED!!")
        return

    if not (1 <= priority <= 10):
        print("Priority must be between 1 and 10!!\tOPERATION CANCELLED!!")
        return

    db.add_subject(subject, priority)

def add_new_chapter():
    # Choosing subjects
    if not (subject_id := helper.choose_subject()): return

    chapter = input("\nEnter Chapter Name: ")
    db.add_chapter(subject_id, chapter)

def add_new_topic():
    # Choosing subject
    if not (subject_id := helper.choose_subject()): return

    # Choosing chapter
    if not (chapter_id := helper.choose_chapter(subject_id)): return

    topic = input("\nEnter Topic Name: ")

    currently_studying = input("\nAre you currently studying this topic? (Y/N): ")
    if currently_studying.lower() == "y":
        currently_studying = True
    else:
        print("Considering that as an NO")
        currently_studying = False

    completed = input("\nDo you want to complete this topic? (Y/N): ")
    if completed.lower() == "y": completed = True
    else:
        print("Considering that as an NO")
        completed = False

    try:
        priority = int(input("Enter Priority (1 - 10): "))
    except ValueError:
        print("Priority must be an integer!!\tOPERATION CANCELLED!!")
        return
    if not (1 <= priority <= 10):
        print("Priority must be between 1 and 10!!\tOPERATION CANCELLED!!")

    db.add_topic(topic, chapter_id, currently_studying, completed, priority)

def add_new_day():
    day = input("\nEnter Day Name: ")
    db.add_day(day)

def add_new_timing():
    # Choosing day
    if not (day_id := helper.choose_day()): return

    from_time = input("\nEnter From time (eg: 12:45am): ")
    try:
        from_time = (datetime.strptime(from_time, "%I:%M%p"))
    except ValueError:
        print("You must use this format -> 2:36pm\tOPERATION CANCELLED!!")
        return

    db.add_time(from_time.hour, from_time.minute, day_id)