# ================================
# SMS Spam Detection - Model Train
# ================================

import pandas as pd
import numpy as np
import nltk
import pickle
import string

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, confusion_matrix

# ----------------------------
# NLTK Resources
# ----------------------------
nltk.download("punkt")
nltk.download("stopwords")

ps = PorterStemmer()
stop_words = set(stopwords.words("english"))

# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv(
    r"C:\Users\RAMAN\Desktop\Spam Detection\spam.csv",
    encoding="latin1"
)

# ----------------------------
# Clean Dataset
# ----------------------------
df.drop(columns=["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], inplace=True)
df.rename(columns={"v1": "target", "v2": "text"}, inplace=True)
df.drop_duplicates(inplace=True)

# ----------------------------
# Encode Target
# ham -> 0 | spam -> 1
# ----------------------------
encoder = LabelEncoder()
df["target"] = encoder.fit_transform(df["target"])

# ----------------------------
# Text Preprocessing Function
# ----------------------------
def transform_text(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)

    processed = []
    for word in tokens:
        if word.isalnum() and word not in stop_words:
            processed.append(ps.stem(word))

    return " ".join(processed)

df["processed_text"] = df["text"].apply(transform_text)

# ----------------------------
# Train-Test Split
# ----------------------------
X = df["processed_text"]
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ----------------------------
# Pipeline (BEST PRACTICE)
# ----------------------------
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=3000)),
    ("model", MultinomialNB())
])

# ----------------------------
# Cross Validation (Precision)
# ----------------------------
cv_precision = cross_val_score(
    pipeline,
    X_train,
    y_train,
    cv=5,
    scoring="precision"
)

print("Cross-Validation Precision Scores:", cv_precision)
print("Average CV Precision:", np.mean(cv_precision))

# ----------------------------
# Train Final Model
# ----------------------------
pipeline.fit(X_train, y_train)

# ----------------------------
# Evaluate on Test Set
# ----------------------------
y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print("\nTest Set Performance")
print("---------------------")
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print("Confusion Matrix:")
print(cm)

# ----------------------------
# Save Model
# ----------------------------
pickle.dump(pipeline, open("backend/spam_model.pkl", "wb"))


print("\nModel saved successfully as spam_model.pkl")
