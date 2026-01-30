# Echo Chamber AI
**Predicting Polarization & Analyzing Social Media Echo Chambers**

Echo Chamber AI is a Natural Language Processing (NLP) application designed to detect the intensity of polarization in digital discourse. This tool uses a fine-tuned **DistilBERT** model to visualize the "echo" effect within communities.

## ✨ Key Features
* **Chameleon UI:** A dynamic Streamlit interface that changes background color based on the polarization score detected by the AI.
* **Real-time Analysis:** Instant classification of messages into **Polarized**, **Neutral**, or **Constructive**.
* **Mass Audit:** Support for CSV file uploads to analyze large datasets and generate community-wide health metrics.
* **Automatic Reset:** The UI automatically reverts to a neutral charcoal gray when switching to data auditing for maximum readability.

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **AI Engine:** Hugging Face Transformers (DistilBERT)
* **Framework:** Streamlit
* **Data Analysis:** Pandas, Plotly

## 🚀 Installation & Usage

```bash
# Clone the repository
git clone [https://github.com/chaymaaa-bh/EchoChamber_AI.git](https://github.com/chaymaaa-bh/EchoChamber_AI.git)

# Enter the directory
cd EchoChamber_AI

# Install dependencies
pip install streamlit pandas transformers torch plotly

# Run the app
streamlit run app.py