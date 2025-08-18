"""Test streamlit app."""

import pytest
from app.score_headlines_api import classify_headlines


def test_app():
    results = classify_headlines(["Headline 1", "Headline 2"])
    assert results == ["Neutral", "Neutral"]
