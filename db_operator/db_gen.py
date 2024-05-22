import sqlite3

# Connecting to SQLite database (or creating it if it doesn't exist)
conn = sqlite3.connect('team_app.db')
cursor = conn.cursor()

# Enabling foreign keys
cursor.execute('PRAGMA foreign_keys = ON')

# Create tables
cursor.execute('''
CREATE TABLE words (
  word_id INTEGER PRIMARY KEY autoincrement,
  russian VARCHAR2 NOT NULL UNIQUE,
  transcription_russian VARCHAR2,
  english VARCHAR2,
  transcription_english VARCHAR2,
  picture BLOB,
  picture_front BLOB,
  picture_back BLOB,
  sound BLOB,
  note1 VARCHAR2,
  note2 VARCHAR2
)
''')

cursor.execute('''
CREATE TABLE topics (
  topic_id INTEGER PRIMARY KEY autoincrement,
  topic_name VARCHAR2 NOT NULL UNIQUE,
  note1 VARCHAR2,
  note2 VARCHAR2
)
''')

cursor.execute('''
CREATE TABLE words_groupings (
  group_id INTEGER PRIMARY KEY autoincrement,
  word_id INTEGER NOT NULL,
  topic_id INTEGER NOT NULL,
  note1 VARCHAR2,
  note2 VARCHAR2,
  FOREIGN KEY(word_id) REFERENCES words(word_id),
  FOREIGN KEY(topic_id) REFERENCES topics(topic_id)
)
''')

cursor.execute('''
CREATE TABLE tests (
  test_id INTEGER PRIMARY KEY autoincrement,
  test_name VARCHAR2 NOT NULL UNIQUE,
  test_type INTEGER,
  note1 VARCHAR2,
  note2 VARCHAR2
)
''')

cursor.execute('''
CREATE TABLE achievemnts (
  achievemnt_id INTEGER PRIMARY KEY autoincrement,
  achievemnt_name VARCHAR2 NOT NULL UNIQUE,
  achievemnt_description VARCHAR2,
  achievemnt_image BLOB,
  note1 VARCHAR2,
  note2 VARCHAR2
)
''')

cursor.execute('''
CREATE TABLE users (
  user_id INTEGER PRIMARY KEY autoincrement,
  nickname VARCHAR2 NOT NULL UNIQUE,
  image BLOB,
  note1 VARCHAR2,
  note2 VARCHAR2
)
''')

cursor.execute('''
CREATE TABLE user_achievemnts (
  user_stat_id INTEGER PRIMARY KEY autoincrement,
  user_id INTEGER,
  achievement_id INTEGER,
  note1 VARCHAR2,
  note2 VARCHAR2,
  FOREIGN KEY(user_id) REFERENCES users(user_id),
  FOREIGN KEY(achievement_id) REFERENCES achievemnts(achievemnt_id)
)
''')

cursor.execute('''
CREATE TABLE lesson (
  lesson_id INTEGER PRIMARY KEY autoincrement,
  topic_id INTEGER,
  done BOOLEAN,
  note1 VARCHAR2,
  note2 VARCHAR2,
  FOREIGN KEY(topic_id) REFERENCES topics(topic_id)
)
''')

cursor.execute('''
CREATE TABLE user_progress (
  progress_id INTEGER PRIMARY KEY autoincrement,
  user_id INTEGER,
  word_id INTEGER,
  lesson_id INTEGER,
  success_counter INTEGER,
  failes_counter INTEGER,
  success_date DATE,
  off_rotation BOOLEAN,
  dictionary BOOLEAN,
  note1 VARCHAR2,
  note2 VARCHAR2,
  FOREIGN KEY(user_id) REFERENCES users(user_id),
  FOREIGN KEY(word_id) REFERENCES words(word_id),
  FOREIGN KEY(lesson_id) REFERENCES lesson(lesson_id)
)
''')

cursor.execute('''
CREATE TABLE testing_stats (
  testing_id INTEGER PRIMARY KEY autoincrement,
  user_id INTEGER,
  test_id INTEGER,
  testing_counter INTEGER,
  note1 VARCHAR2,
  note2 VARCHAR2,
  FOREIGN KEY(user_id) REFERENCES users(user_id),
  FOREIGN KEY(test_id) REFERENCES tests(test_id)
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()
