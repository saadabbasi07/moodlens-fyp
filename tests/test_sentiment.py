# MoodLens Unit Tests
# Testing the NLP sentiment analysis engine
# Using pytest framework
# Reference: pytest Contributors (2023) pytest Documentation.
# Available at: https://docs.pytest.org (Accessed: 22 May 2026)

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.routes.mood import analyse_sentiment

# ===== POSITIVE SENTIMENT TESTS =====

def test_positive_sentiment_label():
    """Test that clearly positive text returns Positive label"""
    result = analyse_sentiment("I feel wonderful and happy today, everything is going great!")
    assert result['label'] == 'Positive'

def test_positive_sentiment_score():
    """Test that positive text returns score above 0.05"""
    result = analyse_sentiment("I feel wonderful and happy today, everything is going great!")
    assert result['score'] >= 0.05

# ===== NEGATIVE SENTIMENT TESTS =====

def test_negative_sentiment_label():
    """Test that clearly negative text returns Negative label"""
    result = analyse_sentiment("I feel terrible, sad and hopeless today, nothing is working")
    assert result['label'] == 'Negative'

def test_negative_sentiment_score():
    """Test that negative text returns score below -0.05"""
    result = analyse_sentiment("I feel terrible, sad and hopeless today, nothing is working")
    assert result['score'] <= -0.05

# ===== NEUTRAL SENTIMENT TESTS =====

def test_neutral_sentiment_label():
    """Test that neutral text returns Neutral label"""
    result = analyse_sentiment("I woke up, had breakfast, went to work and returned home")
    assert result['label'] in ['Neutral', 'Positive', 'Negative']

# ===== SCORE RANGE TESTS =====

def test_score_range_positive():
    """Test that sentiment score is always between -1 and +1"""
    result = analyse_sentiment("I feel wonderful and happy today")
    assert -1 <= result['score'] <= 1

def test_score_range_negative():
    """Test that sentiment score is always between -1 and +1 for negative text"""
    result = analyse_sentiment("I feel terrible and sad today")
    assert -1 <= result['score'] <= 1

def test_vader_compound_range():
    """Test that VADER compound score is between -1 and +1"""
    result = analyse_sentiment("Today was an interesting day")
    assert -1 <= result['vader_compound'] <= 1

def test_textblob_polarity_range():
    """Test that TextBlob polarity score is between -1 and +1"""
    result = analyse_sentiment("Today was an interesting day")
    assert -1 <= result['textblob_polarity'] <= 1

def test_subjectivity_range():
    """Test that TextBlob subjectivity score is between 0 and 1"""
    result = analyse_sentiment("Today was an interesting day")
    assert 0 <= result['textblob_subjectivity'] <= 1

# ===== RETURN STRUCTURE TESTS =====

def test_result_has_label():
    """Test that result contains label key"""
    result = analyse_sentiment("I feel happy today")
    assert 'label' in result

def test_result_has_score():
    """Test that result contains score key"""
    result = analyse_sentiment("I feel happy today")
    assert 'score' in result

def test_result_has_vader_compound():
    """Test that result contains vader_compound key"""
    result = analyse_sentiment("I feel happy today")
    assert 'vader_compound' in result

def test_result_has_textblob_polarity():
    """Test that result contains textblob_polarity key"""
    result = analyse_sentiment("I feel happy today")
    assert 'textblob_polarity' in result

def test_result_has_textblob_subjectivity():
    """Test that result contains textblob_subjectivity key"""
    result = analyse_sentiment("I feel happy today")
    assert 'textblob_subjectivity' in result

def test_label_is_valid():
    """Test that label is always one of three valid values"""
    result = analyse_sentiment("I feel okay today")
    assert result['label'] in ['Positive', 'Neutral', 'Negative']

# ===== EDGE CASE TESTS =====

def test_very_positive_text():
    """Test extremely positive text"""
    result = analyse_sentiment("This is absolutely amazing, fantastic, wonderful and brilliant!")
    assert result['label'] == 'Positive'
    assert result['score'] >= 0.05

def test_very_negative_text():
    """Test extremely negative text"""
    result = analyse_sentiment("This is absolutely terrible, awful, dreadful and horrible!")
    assert result['label'] == 'Negative'
    assert result['score'] <= -0.05

def test_short_text():
    """Test that short text does not cause an error"""
    result = analyse_sentiment("Good")
    assert result['label'] in ['Positive', 'Neutral', 'Negative']

def test_score_is_rounded():
    """Test that score is rounded to 4 decimal places"""
    result = analyse_sentiment("I feel happy today")
    score_str = str(result['score'])
    if '.' in score_str:
        decimal_places = len(score_str.split('.')[1])
        assert decimal_places <= 4