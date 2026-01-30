import pandas as pd
import matplotlib.pyplot as plt

# Charger tes nouveaux résultats
df = pd.read_csv("data/processed/analyzed_echo_results.csv")

# Compter les sentiments
counts = df['sentiment'].value_counts()

# Créer un beau graphique
plt.figure(figsize=(8, 8))
colors = ['#ff4b4b', '#4b4bff'] # Rouge pour LABEL_0, Bleu pour LABEL_1
counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=colors)

plt.title('Analyse de la Chambre d\'Écho (Polarisation des Opinions)')
plt.ylabel('') # Enlever le nom de la colonne
plt.savefig('echo_chamber_evidence.png')
print("📊 BRAVO ! Le graphique 'echo_chamber_evidence.png' est prêt pour votre rapport.")