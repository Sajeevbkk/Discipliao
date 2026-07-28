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
        subjects = cursor.fetchall()
    except Exception as e:
        print(f"Database error: {e}")
        return []
    else:
        if not subjects:
            print("No Subjects Found")
            return []
        return subjects
    finally:
        conn.commit()
        conn.close()

def delete_subject(subject_id):
    conn = get_connection()
    cursor = conn.cursor()

    chapters = get_chapters(subject_id)
    for chapter in chapters:
        # 0 - id
        delete_chapter(chapter[0])

    try:
        cursor.execute("DELETE FROM Subjects WHERE subject_id = ?", (subject_id,))
    except Exception as e:
        print(f"Database error: {e}")
    else:
        print("Subject Deleted Successfully")
    finally:
        conn.commit()
        conn.close()

def add_chapter(name, subject_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Chapters WHERE name = ?", (name,))
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

def get_chapters(subject_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Chapters WHERE subject_id = ?", (subject_id,))
        chapters = cursor.fetchall()
    except Exception as e:
        print(f"Database error: {e}")
        return []
    else:
        if not chapters:
            print("No Chapters Found")
            return []
        return chapters
    finally:
        conn.commit()
        conn.close()

def delete_chapter(chapter_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM Topics WHERE chapter_id = ?", (chapter_id,))
        cursor.execute("DELETE FROM Chapters WHERE chapter_id = ?", (chapter_id,))
    except Exception as e:
        print(f"Database error: {e}")
        return
    else:
        print("Chapter Deleted Successfully")
    finally:
        conn.commit()
        conn.close()

def add_topic(name, chapter_id, currently_studying, completed, priority):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Topics WHERE name = ? AND chapter_id = ?"
                       , (name, chapter_id))
        topic = cursor.fetchone()

        if topic:
            if topic[3] == currently_studying:
                print("Topic Already Exists with same Current Studying!!\tOPERATION CANCELLED!!")
                return
            else:
                print("Topic Already Exists (Updating Current Studying)")
                cursor.execute(
                    "UPDATE Topics SET currently_studying = ? WHERE name = ? AND chapter_id = ?",
                    (currently_studying, name, chapter_id)
                )

            if topic[4] == completed:
                print("Topic Already Exists with Completed Status as same!!\tOPERATION CANCELLED!!")
                return
            else:
                print("Topic Already Exists (Updating Completed Status)")
                cursor.execute(
                    "UPDATE Topics SET completed = ? WHERE name = ? AND chapter_id = ?",
                    (completed, name, chapter_id)
                )

            if topic[5] == priority:
                print("Topic Already Exists with same Priority!!\tOPERATION CANCELLED!!")
                return
            else:
                print("Topic Already Exists (Updating Priority)")
                cursor.execute(
                    "UPDATE Topics SET priority = ? WHERE name = ? AND chapter_id = ?",
                    (priority, name, chapter_id)
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

def get_topics(chapter_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Topics WHERE chapter_id = ?", (chapter_id,))
        topics = cursor.fetchall()
    except Exception as e:
        print(f"Database error: {e}")
        return []
    else:
        if not topics:
            print("No Topics Found")
            return []
        return topics
    finally:
        conn.commit()
        conn.close()

def delete_topic(topic_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM Topics WHERE id = ?", (topic_id,))
    except Exception as e:
        print(f"Database error: {e}")
    else:
        print("Topic Deleted Successfully")
    finally:
        conn.commit()
        conn.close()

def add_day(name):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Days WHERE name = ?", (name,))
        day = cursor.fetchone()

        if not day:
            cursor.execute(
                "INSERT INTO Days (name) VALUES (?)",
                (name,)
            )
        else:
            print("Day Already Exists!!\tOPERATION CANCELLED!!")
            return
    except Exception as e:
        print(f"Database error: {e}")
    else:
        print("Day Added Successfully")
    finally:
        conn.commit()
        conn.close()

def get_days():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Days")
        days = cursor.fetchall()
    except sqlite3.IntegrityError:
        print("Wrong Day ID!!\tOPERATION CANCELLED!!")
        return []
    except Exception as e:
        print(f"Database error: {e}")
    else:
        if not days:
            print("No Days Found!!!\t", end="")
            return []
        return days
    finally:
        conn.commit()
        conn.close()

def delete_day(day_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM Times WHERE day_id = ?", (day_id,))
        cursor.execute("DELETE FROM Days WHERE id = ?", (day_id,))
    except Exception as e:
        print(f"Database error: {e}")
        return
    else:
        print("Day Deleted Successfully")
    finally:
        conn.commit()
        conn.close()

def add_time(from_hour, from_minute, day_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO Times (
                from_hour, from_minute, day_id
            ) VALUES (?, ?, ?)
            """,
            (from_hour, from_minute, day_id)
        )
    except sqlite3.IntegrityError:
        print("Wrong Day ID!!\tOPERATION CANCELLED!!")
        return
    except Exception as e:
        print(f"Database error: {e}")
        return
    finally:
        conn.commit()
        conn.close()

def get_times(day_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Times WHERE day_id = ?", (day_id,))
        times = cursor.fetchall()
    except Exception as e:
        print(f"Database error: {e}")
        return []
    else:
        if not times:
            print("No Times Found")
            return []
        return times
    finally:
        conn.commit()
        conn.close()

def delete_time(time_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Times WHERE id = ?", (time_id,))
    except Exception as e:
        print(f"Database error: {e}")
        return
    else:
        print("Time Deleted Successfully")
    finally:
        conn.commit()
        conn.close()