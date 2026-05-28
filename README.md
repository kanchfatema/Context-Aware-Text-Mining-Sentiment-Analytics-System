# Context-Aware Text Mining & Sentiment Analytics System

A desktop-based Natural Language Processing (NLP) pipeline built in Python that extracts context-specific descriptive features and evaluates multi-part sentiment with calibrated valence thresholds.

## 🚀 Core Architectural Advancements

Standard rule-based sentiment analyzers (like basic VADER configurations) often fail when processing compound sentences separated by adversarial conjunctions (like *but*), or artificially link unrelated words together into meaningless phrases. This project engineered custom solutions to overcome these limitations:

1. **Linguistically Accurate Feature Mining (POS Tagging Shift):** Instead of removing stop words first, this pipeline tags Parts of Speech (`nltk.pos_tag`) on the raw, unedited sentence flow. This isolates distinct linguistic clauses, ensuring the bi-gram engine extracts descriptive expressions (e.g., *Excellent Service*) without creating cross-clause phrase contamination.
2. **Lexicon Bootstrapping & Calibrated Multi-Class Boundaries:** Custom valence adjustments were injected to capture domain-specific complaints. Sharp threshold splits were replaced with a calibrated layout to cleanly segment complex reviews into **Positive**, **Negative**, or **Mixed / Neutral** metrics.

## 🛠️ Tech Stack & Libraries
- **Language:** Python 3.14
- **Interface:** Tkinter & Ttk (Custom Treeview Grid Design)
- **NLP Engine:** NLTK (Tokenization, Perceptron Tagging, VADER Lexicon)

## 📊 Application Dashboard Preview
- **Tab 1: Sentiment Analytics Matrix** – Yields compound normalized scores, descriptive categorization, and real-time positivity/neutrality/negativity ratios.
- **Tab 2: Key Phrases & Context Mining** – Displays extracted structural expressions sorted by usage metrics in a sleek, dynamic UI table.

## 📦 Local Installation & Setup

1. Clone this repository:
   ```bash
   git clone [https://github.com/yourusername/text-analytics-app.git](https://github.com/yourusername/text-analytics-app.git)
   cd text_analytics_app
