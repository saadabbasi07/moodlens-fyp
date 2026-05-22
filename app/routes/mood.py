from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from app import mysql

mood = Blueprint('mood', __name__)

def analyse_sentiment(text):
    # VADER Analysis
    # Reference: Hutto, C. and Gilbert, E. (2014) VADER: A Parsimonious Rule-Based Model
    # for Sentiment Analysis of Social Media Text. AAAI Conference on Weblogs and Social Media.
    vader = SentimentIntensityAnalyzer()
    vader_scores = vader.polarity_scores(text)
    compound = vader_scores['compound']

    # TextBlob Analysis
    # Reference: Loria, S. (2018) TextBlob Documentation.
    # Available at: https://textblob.readthedocs.io (Accessed: 21 May 2026)
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    # Combined score — ensemble approach
    # Both models combined for more accurate sentiment classification
    combined = (compound + polarity) / 2

    # Label assignment based on combined score thresholds
    if combined >= 0.05:
        label = 'Positive'
    elif combined <= -0.05:
        label = 'Negative'
    else:
        label = 'Neutral'

    return {
        'label': label,
        'score': round(combined, 4),
        'vader_compound': round(compound, 4),
        'textblob_polarity': round(polarity, 4),
        'textblob_subjectivity': round(subjectivity, 4)
    }

@mood.route('/')
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT me.*, sd.vader_compound, sd.textblob_polarity, sd.textblob_subjectivity
        FROM mood_entries me
        LEFT JOIN sentiment_details sd ON me.id = sd.entry_id
        WHERE me.user_id = %s
        ORDER BY me.created_at DESC
    """, (current_user.id,))
    entries = cur.fetchall()
    cur.close()

    # Calculate summary statistics for dashboard cards
    total = len(entries)
    positive = sum(1 for e in entries if e['sentiment_label'] == 'Positive')
    negative = sum(1 for e in entries if e['sentiment_label'] == 'Negative')
    neutral = sum(1 for e in entries if e['sentiment_label'] == 'Neutral')

    return render_template('dashboard.html',
        entries=entries,
        total=total,
        positive=positive,
        negative=negative,
        neutral=neutral
    )

@mood.route('/entry', methods=['GET', 'POST'])
@login_required
def entry():
    if request.method == 'POST':
        text = request.form['entry_text']
        result = analyse_sentiment(text)

        cur = mysql.connection.cursor()

        # Insert mood entry into mood_entries table
        cur.execute("""
            INSERT INTO mood_entries (user_id, entry_text, sentiment_label, sentiment_score)
            VALUES (%s, %s, %s, %s)
        """, (current_user.id, text, result['label'], result['score']))
        mysql.connection.commit()

        entry_id = cur.lastrowid

        # Insert detailed NLP scores into sentiment_details table
        cur.execute("""
            INSERT INTO sentiment_details (entry_id, vader_compound, textblob_polarity, textblob_subjectivity)
            VALUES (%s, %s, %s, %s)
        """, (entry_id, result['vader_compound'], result['textblob_polarity'], result['textblob_subjectivity']))
        mysql.connection.commit()
        cur.close()

        flash(f'Mood recorded! Sentiment: {result["label"]}', 'success')
        return redirect(url_for('mood.dashboard'))

    return render_template('entry.html')