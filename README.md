# DocMind 🧠

Une application web qui te permet de **discuter avec tes propres documents**. Uploade un PDF ou un fichier texte, pose tes questions en langage naturel, et obtiens des réponses précises extraites directement de ton contenu.

## Comment ça fonctionne

```
[Document PDF/TXT]
      ↓
  Découpage en chunks (500 tokens)
      ↓
  Génération d'embeddings (OpenAI)
      ↓
  Stockage dans ChromaDB
      ↓
[Question de l'utilisateur]
      ↓
  Recherche des 3 chunks les plus pertinents
      ↓
  GPT-4o-mini génère une réponse basée sur ces extraits
      ↓
[Réponse affichée dans le chat]
```

## Technologies

| Composant | Technologie |
|-----------|-------------|
| Interface | Streamlit |
| LLM | OpenAI GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| Vector Store | ChromaDB |
| Framework RAG | LlamaIndex |
| Lecture PDF | PyMuPDF |

## Installation

**1. Cloner le projet**
```bash
git clone https://github.com/stevkouakam/DocMind.git
cd DocMind
```

**2. Créer un environnement virtuel**
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

**3. Installer les dépendances**
```bash
pip install streamlit llama-index llama-index-llms-openai llama-index-embeddings-openai llama-index-vector-stores-chroma llama-index-readers-file chromadb pymupdf python-dotenv
```

**4. Configurer la clé API**

Crée un fichier `.env` à la racine du projet :
```
OPENAI_API_KEY=ta_cle_openai_ici
```

**5. Lancer l'application**
```bash
streamlit run app.py
```

## Utilisation

1. Ouvre `http://localhost:8501` dans ton navigateur
2. Uploade un fichier PDF ou TXT
3. Pose tes questions dans le chat

## Structure du projet

```
DocMind/
├── app.py          # Interface Streamlit
├── rag.py          # Moteur RAG (indexation + recherche)
├── .env            # Clé API (non commité)
├── .env.example    # Modèle de configuration
├── storage/        # Base vectorielle ChromaDB (non commité)
└── venv/           # Environnement virtuel (non commité)
```

