# Via Claude.ai
import spacy
import math
import re

def count_syllables(word):
    # This is a simple syllable counter and may not be 100% accurate
    return len(
        [
            "".join(g)
            for g in re.findall(r"[aeiou]+|[^aeiou]+", word.lower())
            if g[0] in "aeiou"
        ]
    )

# TH
import statistics
def sentence_lengths(doc):
    """Generate elementary sentence length statistics."""
    s_mean = None
    s_median = None
    s_stdev = None
    s_lengths = []
    for sentence in doc.sents:
        # Punctuation elements are tokens in their own right; remove these from sentence length counts
        s_lengths.append(len([tok.text for tok in sentence if tok.pos_ != "PUNCT"]))

    if s_lengths:
        # If we have at least one measure, we can generate some simple statistics
        s_mean = statistics.mean(s_lengths)
        s_median = statistics.median(s_lengths)
        s_stdev = statistics.stdev(s_lengths) if len(s_lengths) > 1 else 0

    return s_lengths, s_mean, s_median, s_stdev


def text_stats_summary(doc):
    """Generate summary stats report using spaCy."""
    # Basic counts
    n_chars = len(doc.text)
    n_words = len([token for token in doc if not token.is_punct and not token.is_space])
    n_sents = len(list(doc.sents))
    n_unique_words = len(
        set(
            [
                token.text.lower()
                for token in doc
                if not token.is_punct and not token.is_space
            ]
        )
    )

    # Syllable counts
    syllables = [
        count_syllables(token.text)
        for token in doc
        if not token.is_punct and not token.is_space
    ]
    n_syllables = sum(syllables)
    n_monosyllable_words = sum(1 for s in syllables if s == 1)
    n_polysyllable_words = sum(1 for s in syllables if s >= 3)
    n_long_words = sum(
        1
        for token in doc
        if len(token.text) > 6 and not token.is_punct and not token.is_space
    )

    # Sentence length statistics
    s_lengths, s_mean, s_median, s_stdev = sentence_lengths(doc)
    counts = {
        "n_chars": n_chars,
        "n_words": n_words,
        "n_sents": n_sents,
        "n_unique_words": n_unique_words,
        "n_syllables": n_syllables,
        "n_monosyllable_words": n_monosyllable_words,
        "n_polysyllable_words": n_polysyllable_words,
        "n_long_words": n_long_words,
        "sentence_length_mean": s_mean,
        "sentence_length_median": s_median,
        "sentence_length_stdev": s_stdev,
        "sentence_legths": s_lengths
    }

    # Readability metrics
    if n_words > 0 and n_sents > 0:
        # Flesch Reading Ease
        flesch_reading_ease = (
            206.835 - 1.015 * (n_words / n_sents) - 84.6 * (n_syllables / n_words)
        )

        # Flesch-Kincaid Grade Level
        flesch_kincaid_grade_level = (
            0.39 * (n_words / n_sents) + 11.8 * (n_syllables / n_words) - 15.59
        )

        # Automated Readability Index
        automated_readability_index = (
            4.71 * (n_chars / n_words) + 0.5 * (n_words / n_sents) - 21.43
        )

        # Coleman-Liau Index
        l = (n_chars / n_words) * 100
        s = (n_sents / n_words) * 100
        coleman_liau_index = 0.0588 * l - 0.296 * s - 15.8

        # SMOG Index
        if n_sents >= 30:
            smog_index = (
                1.0430 * math.sqrt(n_polysyllable_words * (30 / n_sents)) + 3.1291
            )
        else:
            smog_index = None

        # Gunning Fog Index
        gunning_fog_index = 0.4 * (
            (n_words / n_sents) + 100 * (n_polysyllable_words / n_words)
        )

        readability = {
            "flesch_reading_ease": flesch_reading_ease,
            "flesch_kincaid_grade_level": flesch_kincaid_grade_level,
            "automated_readability_index": automated_readability_index,
            "coleman_liau_index": coleman_liau_index,
            "smog_index": smog_index,
            "gunning_fog_index": gunning_fog_index,
        }
    else:
        readability = {}

    return counts, readability

# Example usage
def analyze_text(text):
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    counts, readability = text_stats_summary(doc)
    print("Counts:", counts)
    print("Readability:", readability)


# Claude.ai

import spacy
from collections import defaultdict


def extract_acronyms(doc):
    """
    Extract acronyms and their possible definitions from a spaCy Doc object.

    Args:
    doc (spacy.tokens.Doc): A spaCy Doc object

    Returns:
    dict: A dictionary of acronyms and their possible definitions
    """
    acronym_dict = defaultdict(list)

    # Find potential acronyms (uppercase words with 2-5 letters)
    acronyms = [
        token.text
        for token in doc
        if token.text.isupper() and 2 <= len(token.text) <= 5
    ]

    # Find potential definitions
    for sent in doc.sents:
        for i, token in enumerate(sent):
            if token.text == "(" and i > 0:
                prev_tokens = sent[max(0, i - 5) : i]
                next_token = sent[i + 1] if i + 1 < len(sent) else None

                if next_token and next_token.text in acronyms:
                    # Check if the previous words match the acronym
                    potential_def = " ".join([t.text for t in prev_tokens])
                    if next_token.text == "".join(
                        word[0].upper()
                        for word in potential_def.split()
                        if word[0].isalpha()
                    ):
                        acronym_dict[next_token.text].append(potential_def)

                elif prev_tokens[-1].text in acronyms:
                    # Check if the next words match the acronym
                    potential_def = []
                    for j in range(i + 1, min(i + 6, len(sent))):
                        if sent[j].text == ")":
                            break
                        potential_def.append(sent[j].text)
                    potential_def = " ".join(potential_def)
                    if prev_tokens[-1].text == "".join(
                        word[0].upper()
                        for word in potential_def.split()
                        if word[0].isalpha()
                    ):
                        acronym_dict[prev_tokens[-1].text].append(potential_def)

    return dict(acronym_dict)


import spacy
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
except:
    print("Problem with sklearn")
from collections import defaultdict
import numpy as np


def extract_keyterms_tfidf(doc, n=10):
    """
    Extract key terms from a list of spaCy Doc objects using TF-IDF.

    Args:
    docs (list): A list of spaCy Doc objects
    n (int): Number of top terms to return

    Returns:
    list: A list of tuples (term, score) for the top n terms
    """
    # Preprocess: extract lemmatized tokens, excluding stopwords and punctuation
    processed_doc =  " ".join(
            [
                token.lemma_.lower()
                for token in doc
                if not token.is_stop and not token.is_punct and token.is_alpha
            ]
        )
       
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_doc)

    # Get feature names (terms)
    feature_names = np.array(vectorizer.get_feature_names_out())

    # Calculate the average TF-IDF score for each term across all documents
    avg_tfidf_scores = np.mean(tfidf_matrix.toarray(), axis=0)

    # Sort terms by their average TF-IDF score
    sorted_indices = np.argsort(avg_tfidf_scores)[::-1]
    top_terms = feature_names[sorted_indices][:n]
    top_scores = avg_tfidf_scores[sorted_indices][:n]

    return list(zip(top_terms, top_scores))


def extract_keyterms(doc, n=10):
    """
    Extract key terms using both TF-IDF and noun phrase extraction.

    Args:
    docs (list): A list of spaCy Doc objects
    n (int): Number of top terms to return

    Returns:
    list: A list of tuples (term, score) for the top n terms
    """
    # Extract TF-IDF based key terms
    tfidf_terms = extract_keyterms_tfidf(doc, n)

    # Extract noun phrases
    noun_phrases = defaultdict(int)
    for chunk in doc.noun_chunks:
        if not all(token.is_stop for token in chunk):
            noun_phrases[chunk.lemma_.lower()] += 1

    # Combine TF-IDF terms and noun phrases
    combined_terms = defaultdict(float)
    for term, score in tfidf_terms:
        combined_terms[term] += score

    for phrase, count in noun_phrases.items():
        if phrase not in combined_terms:
            combined_terms[phrase] += count  # Normalize by document count

    # Sort and return top n terms
    return sorted(combined_terms.items(), key=lambda x: x[1], reverse=True)[:n]


