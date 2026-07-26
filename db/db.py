import sqlite3

def get_connection():
    conn = sqlite3.connect('data.db')
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def add_subject(name, priority):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM subjects WHERE name = ?", (name,))
        subject = cursor.fetchone()

        if subject:
            if subject[2] == priority:
                print("Subject Already Exists with Same Priority!!\tOPERATION CANCELLED!!")
                return
            else:
                print("Subject Already Exists (Updating priority)")
                cursor.execute(
                    "UPDATE subjects SET priority = ? WHERE name = ?",
                    (priority, name)
                )
        else:
            cursor.execute(
                "INSERT INTO Subjects (name, priority) VALUES (?, ?)",
                (name, priority)
            )
    except Exception as e:
        print(f"Database error: {e}")
    else:
        print("Subject Added Successfully")
    finally:
        conn.commit()
        conn.close()

def get_subjects():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Subjects")
    except Exception as e:
        print(f"Database error: {e}")
        return []
    else:
        return cursor.fetchall() # subjects list
    finally:
        conn.commit()
        conn.close()

def add_chapter(name, subject_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Chapters WHERE name = ?", name)
        chapter = cursor.fetchone()

        if chapter:
            if chapter[2] == subject_id:
                print("Chapter Already Exists with Same Subject ID!!\tOPERATION CANCELLED!!")
                return
            else:
                print("Chapter Already Exists (Updating Subject ID)")
                cursor.execute(
                    "UPDATE Chapters SET subject_id = ? WHERE name = ?",
                    (subject_id, name)
                )
        else:
            cursor.execute(
                "INSERT INTO Chapters (name, subject_id) VALUES (?, ?)",
                (name, subject_id)
            )
    except sqlite3.IntegrityError:
        print("Wrong Subject ID!!\tOPERATION CANCELLED!!")
        return
    except Exception as e:
        print(f"Database error: {e}")
    else:
        print("Chapter Added Successfully")
    finally:
        conn.commit()
        conn.close()

def get_chapters():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Chapters")
    except Exception as e:
        print(f"Database error: {e}")
        return []
    else:
        return cursor.fetchall() # chapters list
    finally:
        conn.commit()
        conn.close()

def add_topic(name, chapter_id, currently_studying, priority):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Topics WHERE name = ?", name)
        topic = cursor.fetchone()

        if topic:
            if topic[2] == chapter_id:
                print("Topic Already Exists with same Chapter ID!!\tOPERATION CANCELLED!!")
                return
            else:
                print("Topic Already Exists (Updating Chapter ID)")
                cursor.execute(
                    "UPDATE Topics SET chapter_id = ? WHERE name = ?",
                    (chapter_id, name)
                )

            if topic[3] == currently_studying:
                print("Topic Already Exists with same Current Studying!!\tOPERATION CANCELLED!!")
                return
            else:
                print("Topic Already Exists (Updating Current Studying)")
                cursor.execute(
                    "UPDATE Topics SET currently_studying = ? WHERE name = ?",
                    (currently_studying, name)
                )

            if topic[4] == priority:
                print("Topic Already Exists with same Priority!!\tOPERATION CANCELLED!!")
                return
            else:
                print("Topic Already Exists (Updating Priority)")
                cursor.execute(
                    "UPDATE Topics SET priority = ? WHERE name = ?",
                    (priority, name)
                )
        else:
            cursor.execute(
                "INSERT INTO Topics (name, chapter_id, currently_studying, priority) VALUES (?, ?, ?, ?)",
                (name, chapter_id, currently_studying, priority)
            )
    except sqlite3.IntegrityError:
        print("Wrong Chapter ID!!\tOPERATION CANCELLED!!")
        return
    except Exception as e:
        print(f"Database error: {e}")
        return
    else:
        print("Topic Added Successfully")
    finally:
        conn.commit()
        conn.close()
