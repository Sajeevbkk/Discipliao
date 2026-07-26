from xmlrpc.client import Boolean

from db import db

def read_input():
    while True:
        print("\nChoose an option:")
        print("\t0 - Quit")
        print("\t1 - Add New Subject")
        print("\t2 - Add New Chapter")
        print("\t3 - Add New Topic")
        print("\t4 - Get Time Table")

        try:
            option = int(input(" : "))
        except ValueError:
            print("Please enter a number!!\tOPERATION CANCELLED!!")
            continue

        match option:
            case 0:
                break
            case 1:
                add_new_subject()
            case 2:
                add_new_chapter()
            case 3:
                add_new_topic()
            case _:
                print("Considering as Exit!!")
                break


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
    chapter = input("\nEnter Chapter Name: ")
    subjects = db.get_subjects()
    if not subjects:
        print("No subjects found!!!\tAdd Subjects to Continue!!")
        return

    subject_ids = []

    print("Choose a subject for this chapter:")
    for subject_id, subject, _ in subjects:
        subject_ids.append(subject_id)
        print(f"\t{subject_id} - {subject}")
    try:
        subject_id = int(input("Enter Subject ID: "))
    except ValueError:
        print("Subject ID must be an integer!!\tOPERATION CANCELLED!!")
        return

    if subject_id not in subject_ids:
        print("Subject ID is invalid!!\tOPERATION CANCELLED!!")
        return

    db.add_chapter(subject_id, chapter)

def add_new_topic():
    topic = input("\nEnter Topic Name: ")
    chapters = db.get_chapters()
    if not chapters:
        print("No chapters found!!!\tAdd Chapters to Continue!!")
        return

    chapter_ids = []
    print("Choose a chapter for this topic:")
    for chapter_id, chapter, _ in chapters:
        chapter_ids.append(chapter_id)
        print(f"\t{chapter_id} - {chapter}")
    try:
        chapter_id = int(input("Enter Chapter ID: "))
    except ValueError:
        print("Chapter ID must be an integer!!\tOPERATION CANCELLED!!")
        return

    if chapter_id not in chapter_ids:
        print("Chapter ID is invalid!!\tOPERATION CANCELLED!!")
        return

    currently_studying = input("\nAre you currently studying this topic? (Y/N): ")
    if currently_studying.lower() == "y":
        currently_studying = True
    else:
        print("Considering that as an NO")
        currently_studying = False

    try:
        priority = int(input("Enter Priority (1 - 10): "))
    except ValueError:
        print("Priority must be an integer!!\tOPERATION CANCELLED!!")
        return
    if not (1 <= priority <= 10):
        print("Priority must be between 1 and 10!!\tOPERATION CANCELLED!!")

    db.add_topic(topic, chapter_id, currently_studying, priority)
