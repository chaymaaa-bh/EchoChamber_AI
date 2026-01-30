import pandas as pd
import re
import os

def clean_text(text):
    """
    Nettoyage spécifique pour les commentaires Reddit.
    """
    if pd.isna(text):
        return ""
    
    # 1. Mise en minuscule
    text = text.lower()
    
    # 2. Supprimer les messages automatiques de Reddit
    text = re.sub(r'\[deleted\]|\[removed\]', '', text)
    
    # 3. Supprimer les URLs (http, https, www)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # 4. Supprimer les caractères spéciaux et la ponctuation excessive
    # On garde les lettres et les chiffres de base
    text = re.sub(r'[^a-z0-9\s!\?]', '', text)
    
    # 5. Supprimer les espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_dataset(input_path, output_path):
    print(f"--- Démarrage du Preprocessing ---")
    df = pd.read_csv(input_path)
    
    # On applique le nettoyage
    print("Nettoyage de la colonne 'body'...")
    df['clean_body'] = df['body'].apply(clean_text)
    
    # On supprime les lignes qui se retrouvent vides après nettoyage
    initial_len = len(df)
    df = df[df['clean_body'] != ""]
    print(f"Lignes supprimées car vides : {initial_len - len(df)}")
    
    # Sauvegarde
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Succès ! Fichier nettoyé sauvegardé dans : {output_path}")

if __name__ == "__main__":
    INPUT = 'data/processed/full_dataset.csv'
    OUTPUT = 'data/processed/cleaned_dataset.csv'
    preprocess_dataset(INPUT, OUTPUT)