from .db import get_connection

conn = get_connection()
c = conn.cursor()

c.execute(
    """
    CREATE TABLE IF NOT EXISTS Subjects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        priority INTEGER NOT NULL
    )
    """
)

c.execute(
    """
    CREATE TABLE IF NOT EXISTS Chapters(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        subject_id INTEGER NOT NULL,
        FOREIGN KEY(subject_id) REFERENCES Subjects(id)
    )
    """
)

c.execute(
    """
    CREATE TABLE IF NOT EXISTS Topics(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        chapter_id INTEGER NOT NULL,
        currently_studying BOOLEAN NOT NULL,
        priority INTEGER NOT NULL,
        FOREIGN KEY(chapter_id) REFERENCES Chapters(id)
    )
    """
)

conn.commit()
conn.close()