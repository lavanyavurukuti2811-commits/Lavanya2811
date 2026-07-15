from deep_translator import MyMemoryTranslator
from flask import Flask, render_template, request, redirect, url_for
import os
import json
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

# Installation requirement: pip install transformers torch textblob deep-translator

from transformers import pipeline
from textblob import TextBlob
import torch
app = Flask(__name__)
users = []
@dataclass
class SentimentResult:
    """Data class to store sentiment analysis results"""
    text: str
    translated_text: str
    language: str
    sentiment: str
    confidence: float
    polarity: float
    subjectivity: float
    timestamp: str

class MultilingualSentimentAnalyzer:
    """
    A comprehensive sentiment analyzer for e-commerce platforms
    that supports multiple languages
    """
    
    def __init__(self):
        """Initialize sentiment analysis models"""
        print("Initializing multilingual sentiment analyzer...")
        
        # Using a multilingual model that works across many languages
        self.multilingual_pipeline = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment",
            device=0 if torch.cuda.is_available() else -1
        )
        
        print("✓ Multilingual model loaded successfully")
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of the text
        Supported languages: English, French, German, Spanish, Italian, etc.
        """
        try:
            blob = TextBlob(text)
            detected_lang = blob.detect_language()
            return detected_lang
        except Exception as e:
            print(f"Language detection failed: {e}")
            return "en"
    
    def translate_to_english(self, text: str, source_language: str) -> str:
        """
        Translate text to English using MyMemoryTranslator
        
        Args:
            text: Text to translate
            source_language: Language code of the source text
        
        Returns:
            Translated text in English
        """
        if source_language == 'en':
            return text
        
        try:
            # Use MyMemoryTranslator which is more reliable than GoogleTranslator
            translator = MyMemoryTranslator(source_language=source_language, target_language='en')
            translated_text = translator.translate(text)
            print(f"✓ Translated from {source_language} to English: {translated_text}")
            return translated_text
        except Exception as e:
            print(f"❌ Translation failed for language {source_language}: {e}")
            return text  # Return original text if translation fails
    
    def analyze_sentiment(self, text: str, language: str = None) -> SentimentResult:
        """
        Analyze sentiment of a given text
        
        Args:
            text: Text to analyze
            language: Language code (optional, auto-detected if not provided)
        
        Returns:
            SentimentResult object with detailed sentiment information
        """
        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string")
        
        # Auto-detect language if not provided
        if language is None:
            language = self.detect_language(text)
        
        # Translate to English
        translated_text = self.translate_to_english(text, language)
        
        # Truncate text if too long (models have token limits)
        max_length = 512
        truncated_text = translated_text[:max_length]
        
        # Get sentiment from transformer model
        prediction = self.multilingual_pipeline(truncated_text, truncation=True)
        model_sentiment = prediction[0]
        
        # Get polarity and subjectivity using TextBlob
        blob = TextBlob(translated_text)
        polarity = blob.sentiment.polarity  # Range: -1 to 1
        subjectivity = blob.sentiment.subjectivity  # Range: 0 to 1
        
        # Map model output to readable sentiment
        label = model_sentiment['label']
        confidence = round(model_sentiment['score'], 4)
        # Convert star rating to sentiment
        stars = int(label.split()[0])
        
        # Normalize sentiment label
        if stars <= 2:
            sentiment = 'NEGATIVE'
        elif stars == 3:
            sentiment = 'NEUTRAL'
        else:
            sentiment = 'POSITIVE'
        
        result = SentimentResult(
            text=text,
            translated_text=translated_text,
            language=language,
            sentiment=sentiment,
            confidence=confidence,
            polarity=polarity,
            subjectivity=subjectivity,
            timestamp=datetime.now().isoformat()
        )
        
        return result
    
    def analyze_batch(self, texts: List[str], languages: List[str] = None) -> List[SentimentResult]:
        """
        Analyze sentiment for multiple texts
        
        Args:
            texts: List of texts to analyze
            languages: List of language codes (optional)
        
        Returns:
            List of SentimentResult objects
        """
        results = []
        languages = languages or [None] * len(texts)
        
        for text, lang in zip(texts, languages):
            try:
                result = self.analyze_sentiment(text, lang)
                results.append(result)
            except Exception as e:
                print(f"Error analyzing text: {e}")
                continue
        
        return results
    
    def get_sentiment_distribution(self, results: List[SentimentResult]) -> Dict[str, int]:
        """
        Get distribution of sentiments from results
        
        Args:
            results: List of SentimentResult objects
        
        Returns:
            Dictionary with sentiment counts
        """
        distribution = {
            'POSITIVE': 0,
            'NEGATIVE': 0,
            'NEUTRAL': 0
        }
        
        for result in results:
            distribution[result.sentiment] += 1
        
        return distribution
    
    def generate_report(self, results: List[SentimentResult]) -> Dict:
        """
        Generate a comprehensive sentiment analysis report
        
        Args:
            results: List of SentimentResult objects
        
        Returns:
            Dictionary containing analysis report
        """
        if not results:
            return {}
        
        distribution = self.get_sentiment_distribution(results)
        total = len(results)
        
        # Calculate metrics
        avg_polarity = sum(r.polarity for r in results) / total
        avg_confidence = sum(r.confidence for r in results) / total
        avg_subjectivity = sum(r.subjectivity for r in results) / total
        
        # Language distribution
        language_dist = {}
        for result in results:
            lang = result.language
            language_dist[lang] = language_dist.get(lang, 0) + 1
        
        report = {
            'total_analyzed': total,
            'analysis_timestamp': datetime.now().isoformat(),
            'sentiment_distribution': distribution,
            'sentiment_percentages': {
                k: round((v / total) * 100, 2) for k, v in distribution.items()
            },
            'average_polarity': round(avg_polarity, 4),
            'average_confidence': round(avg_confidence, 4),
            'average_subjectivity': round(avg_subjectivity, 4),
            'language_distribution': language_dist
        }
        
        return report
    
    def save_results(self, results: List[SentimentResult], filename: str = "sentiment_results.json"):
        """Save analysis results to JSON file"""
        data = [asdict(r) for r in results]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Results saved to {filename}")


# Example usage
def main():
    """Demonstrate the sentiment analyzer"""
    
    # Initialize analyzer
    analyzer = MultilingualSentimentAnalyzer()
    
    # Sample e-commerce reviews in multiple languages
    reviews = [
        # English
        "This product is amazing! Best purchase ever. Highly recommend!",
        "Terrible quality. Broke within a week. Very disappointed.",
        "It's okay. Nothing special but does the job.",
        
        # Spanish
        "¡Producto excelente! Entrega rápida y empaque perfecto.",
        "Mala calidad. No recomiendo este producto.",
        
        # French
        "Très satisfait de mon achat. Qualité exceptionnelle!",
        "Décevant. Pas conforme à la description.",
        
        # German
        "Ausgezeichnetes Produkt! Kann ich nur empfehlen.",
        "Schlechte Qualität und schlechter Service.",
    ]
    
    print("\n" + "="*60)
    print("MULTILINGUAL SENTIMENT ANALYSIS FOR E-COMMERCE")
    print("="*60 + "\n")
    
    # Analyze each review
    print("Analyzing individual reviews...\n")
    results = []
    for i, review in enumerate(reviews, 1):
        result = analyzer.analyze_sentiment(review)
        results.append(result)
        
        print(f"Review {i}:")
        print(f"  Original Text: {review}")
        print(f"  Translated Text: {result.translated_text}")
        print(f"  Language: {result.language}")
        print(f"  Sentiment: {result.sentiment} (Confidence: {result.confidence})")
        print(f"  Polarity: {result.polarity:.3f} | Subjectivity: {result.subjectivity:.3f}")
        print()
    
    # Generate report
    print("\n" + "="*60)
    print("ANALYSIS REPORT")
    print("="*60 + "\n")
    
    report = analyzer.generate_report(results)
    
    print(f"Total Reviews Analyzed: {report['total_analyzed']}")
    print(f"\nSentiment Distribution:")
    for sentiment, count in report['sentiment_distribution'].items():
        percentage = report['sentiment_percentages'][sentiment]
        print(f"  {sentiment}: {count} ({percentage}%)")
    
    print(f"\nAverage Metrics:")
    print(f"  Polarity: {report['average_polarity']:.4f}")
    print(f"  Confidence: {report['average_confidence']:.4f}")
    print(f"  Subjectivity: {report['average_subjectivity']:.4f}")
    
    print(f"\nLanguage Distribution:")
    for lang, count in report['language_distribution'].items():
        print(f"  {lang}: {count}")
    
    # Save results
    analyzer.save_results(results)
    
    print("\n" + "="*60)
    print("Analysis complete!")
    print("="*60 + "\n")


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        for user in users:
            if user["email"] == email and user["password"] == password:
                return redirect(url_for("user_home"))

        return "Invalid Email or Password"

    return render_template("login.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        users.append({
            "name": name,
            "email": email,
            "password": password
        })

        print(users)   # Shows registered users in the terminal

        return redirect(url_for("login"))

    return render_template("registration.html")

@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

@app.route("/dataset")
def dataset():
    return render_template("dataset.html")

@app.route("/user_home")
def user_home():
    return render_template("user_home.html")

if __name__ == "__main__":
    # Run sentiment analysis demonstration
    main()
    
    # Uncomment the line below to run Flask web server instead
    # app.run(debug=True)
