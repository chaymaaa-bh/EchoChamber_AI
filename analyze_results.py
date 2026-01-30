import pandas as pd
from transformers import pipeline
import os

# Chemins vers tes dossiers
data_in = "data/processed/cleaned_dataset.csv"
model_path = "models/sentiment_model"
data_out = "data/processed/analyzed_echo_results.csv"

print("🤖 Chargement du modèle à 91%...")
# On charge l'IA que tu as entraînée
classifier = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)

# On vérifie si ton dataset existe
if not os.path.exists(data_in):
    print(f"❌ Erreur : Je ne trouve pas le fichier {data_in}")
else:
    df = pd.read_csv(data_in)
    print(f"🔍 Analyse de {len(df.head(100))} lignes en cours...")

    def get_sentiment(text):
        if pd.isna(text) or str(text).strip() == "": return "NEUTRAL", 0
        res = classifier(str(text), truncation=True)[0]
        return res['label'], res['score']

    # On analyse les 100 premières lignes pour tester si ça marche
    subset = df.head(100).copy()
    results = subset['clean_body'].apply(get_sentiment)
    subset['sentiment'] = [r[0] for r in results]
    subset['confidence'] = [r[1] for r in results]

    # Sauvegarde du nouveau fichier avec les preuves
    os.makedirs(os.path.dirname(data_out), exist_ok=True)
    subset.to_csv(data_out, index=False)
    
    print(f"✅ Fichier créé : {data_out}")
    print("\n📊 RÉSULTATS POUR TON GROUPE :")
    print(subset['sentiment'].value_counts(normalize=True) * 100)