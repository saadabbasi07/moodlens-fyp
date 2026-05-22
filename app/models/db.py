# MoodLens Database Models
# This file defines the database connection and query functions
# MySQL is used as the relational database management system
# Reference: Oracle Corporation (2023) MySQL 8.0 Reference Manual.
# Available at: https://dev.mysql.com/doc/refman/8.0/en/ (Accessed: 21 May 2026)

from app import mysql

def get_user_by_email(email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    return user

def get_user_by_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    return user

def create_user(username, email, password_hash):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
        (username, email, password_hash)
    )
    mysql.connection.commit()
    cur.close()

def get_mood_entries(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT me.*, sd.vader_compound, sd.textblob_polarity, sd.textblob_subjectivity
        FROM mood_entries me
        LEFT JOIN sentiment_details sd ON me.id = sd.entry_id
        WHERE me.user_id = %s
        ORDER BY me.created_at DESC
    """, (user_id,))
    entries = cur.fetchall()
    cur.close()
    return entries

def save_mood_entry(user_id, text, label, score):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO mood_entries (user_id, entry_text, sentiment_label, sentiment_score)
        VALUES (%s, %s, %s, %s)
    """, (user_id, text, label, score))
    mysql.connection.commit()
    entry_id = cur.lastrowid
    cur.close()
    return entry_id

def save_sentiment_details(entry_id, vader, polarity, subjectivity):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO sentiment_details (entry_id, vader_compound, textblob_polarity, textblob_subjectivity)
        VALUES (%s, %s, %s, %s)
    """, (entry_id, vader, polarity, subjectivity))
    mysql.connection.commit()
    cur.close()