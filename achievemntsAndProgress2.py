import sqlite3

db_path = "team_app.db"

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                achievement_id INTEGER PRIMARY KEY,
                achievement_name VARCHAR2 NOT NULL,
                achievement_description VARCHAR2,
                achievement_image BLOB,
                note1 VARCHAR2,
                note2 VARCHAR2
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_achievements (
                user_stat_id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                achievement_id INTEGER NOT NULL,
                note1 VARCHAR2,
                note2 VARCHAR2,
                FOREIGN KEY(user_id) REFERENCES users(user_id),
                FOREIGN KEY(achievement_id) REFERENCES achievements(achievement_id)
            )
        ''')
        conn.commit()
        conn.close()

    def add_achievement(self, name, description, image=None, note1=None, note2=None):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO achievements (achievement_name, achievement_description, achievement_image, note1, note2)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, description, image, note1, note2))
        conn.commit()
        conn.close()

    def get_achievements(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM achievements')
        achievements = cursor.fetchall()
        conn.close()
        return achievements

    def add_user_achievement(self, user_id, achievement_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_achievements (user_id, achievement_id)
            VALUES (?, ?)
        ''', (user_id, achievement_id))
        conn.commit()
        conn.close()

    def get_user_achievements(self, user_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT achievements.achievement_id, achievements.achievement_name, achievements.achievement_description
            FROM user_achievements
            JOIN achievements ON user_achievements.achievement_id = achievements.achievement_id
            WHERE user_achievements.user_id = ?
        ''', (user_id,))
        user_achievements = cursor.fetchall()
        conn.close()
        return user_achievements

    def get_users(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users')
        users = cursor.fetchall()
        conn.close()
        return users

    def check_all_users_achievements(self):
        users = self.get_users()
        for user in users:
            user_id = user[0]
            self.check_user_achievements(user_id)

    def check_user_achievements(self, user_id):
        achievements = self.get_achievements()
        for achievement in achievements:
            criteria = achievement[4]  # Изменение индекса для корректного доступа к note1
            if self._criteria_met(user_id, criteria):
                self.add_user_achievement(user_id, achievement[0])
                print(f"User {user_id} unlocked achievement '{achievement[1]}'")

    def _criteria_met(self, user_id, criteria):
        conn = self._connect()
        cursor = conn.cursor()

        if criteria == "first_task_completed":
            cursor.execute('SELECT COUNT(*) FROM user_progress WHERE user_id = ? AND success_counter > 0', (user_id,))
            result = cursor.fetchone()[0]
            return result > 0

        elif criteria == "100_words_learned":
            cursor.execute('SELECT COUNT(*) FROM user_progress WHERE user_id = ? AND success_counter > 0', (user_id,))
            result = cursor.fetchone()[0]
            return result >= 100

        elif criteria == "10_lessons_completed":
            cursor.execute('SELECT COUNT(*) FROM lesson WHERE user_id = ? AND done = 1', (user_id,))
            result = cursor.fetchone()[0]
            return result >= 10

        # Добавить остальные критерии здесь
        conn.close()
        return False

class Achievement:
    def __init__(self, db_manager, name, description, image=None, note1=None, note2=None):
        self.db_manager = db_manager
        self.name = name
        self.description = description
        self.image = image
        self.note1 = note1
        self.note2 = note2

    def save(self):
        self.db_manager.add_achievement(self.name, self.description, self.image, self.note1, self.note2)

class UserAchievement:
    def __init__(self, db_manager, user_id, achievement_id):
        self.db_manager = db_manager
        self.user_id = user_id
        self.achievement_id = achievement_id

    def save(self):
        self.db_manager.add_user_achievement(self.user_id, self.achievement_id)

def check_achievement_criteria(db_manager, user_id, criteria):
    # Логика проверки выполнения условий для получения ачивки
    achievements = db_manager.get_achievements()
    for achievement in achievements:
        if achievement[4] == criteria:  # note1 хранится в 5-й колонке
            user_achievement = UserAchievement(db_manager, user_id, achievement[0])
            user_achievement.save()
            print(f"Achievement '{achievement[1]}' unlocked!")  # name хранится во 2-й колонке

class ProgressSchool:
    def __init__(self, db_path):
        self.db_manager = DatabaseManager(db_path)

    def get_topic_progress(self, user_id):
        conn = self.db_manager._connect()
        cursor = conn.cursor()

        # Получение всех тем
        cursor.execute('SELECT topic_id, topic_name FROM topics')
        topics = cursor.fetchall()

        progress_report = []

        for topic in topics:
            topic_id, topic_name = topic

            # Получение всех слов в теме
            cursor.execute('''
                SELECT COUNT(*) FROM words_groupings
                WHERE topic_id = ?
            ''', (topic_id,))
            total_words = cursor.fetchone()[0]

            # Получение количества изученных слов в теме
            cursor.execute('''
                SELECT COUNT(*) FROM words_groupings wg
                JOIN user_progress up ON wg.word_id = up.word_id
                WHERE wg.topic_id = ? AND up.user_id = ? AND up.success_counter > 0
            ''', (topic_id, user_id))
            learned_words = cursor.fetchone()[0]

            progress_report.append({
                'topic_id': topic_id,
                'topic_name': topic_name,
                'total_words': total_words,
                'learned_words': learned_words,
                'remaining_words': total_words - learned_words
            })

        conn.close()
        return progress_report

if __name__ == "__main__":
    db_manager = DatabaseManager(db_path)

    # Примеры добавления ачивок
    achievements = [
        Achievement(db_manager, "Первый шаг", "Завершил первый урок", note1="first_task_completed"),
        Achievement(db_manager, "Полиглот", "Выучил 100 слов", note1="100_words_learned"),
        Achievement(db_manager, "Учитель", "Завершил 10 уроков", note1="10_lessons_completed"),
        Achievement(db_manager, "Лингвист", "Выучил все слова из одной темы"),
        Achievement(db_manager, "Испытатель", "Пройдено 5 тестов")
    ]

    for achievement in achievements:
        achievement.save()

    # Проверка выполнения критериев для всех пользователей
    db_manager.check_all_users_achievements()

    # Пример использования школы прогресса
    progress_school = ProgressSchool(db_path)
    report = progress_school.get_topic_progress(user_id)
    for topic in report:
        print(f"Тема: {topic['topic_name']}")
        print(f"Изучено слов: {topic['learned_words']}/{topic['total_words']}")
        print(f"Осталось слов: {topic['remaining_words']}\n")
