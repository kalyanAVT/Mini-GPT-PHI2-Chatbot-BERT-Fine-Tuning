# 🤖 BERT-GPT Streamlit Chatbot

An intelligent sentiment-aware chatbot that blends the power of **fine-tuned BERT for sentiment analysis**, **local Phi-2 LLM (via Hugging Face)**, and **GPT-3.5/4 (via OpenAI API)**. Built with a clean and interactive **Streamlit UI** and equipped with **Text-to-Speech**, this app enables flexible response generation with both local and cloud-based models.

---

## 🔥 Features

- 🧠 **Fine-tuned BERT** sentiment classifier
- 💬 **Local Phi-2 LLM** response generation (no internet required after download)
- 🌐 **GPT-3.5/GPT-4 support** via OpenAI API
- 🎨 Beautiful chat UI with animated sentiment-based borders
- 🔊 **TTS support** using `gTTS`
- 📁 Ready for **Google Colab** and **GitHub + Streamlit Cloud** deployment
- 🧪 Built-in **Easter Eggs** for fun geeky interactions

---

## 🧰 Tech Stack

- Python 3.10+
- Streamlit
- Hugging Face Transformers
- PyTorch
- gTTS (Text-to-Speech)
- Git LFS (for large model storage)
- Google Colab (optional run)

---

## 🧠 Models Used

- `bert-base-uncased` (fine-tuned for sentiment)
- `microsoft/phi-2` (loaded locally)
- Optional GPT model via OpenAI API

---
## 🚀 Demo

> 🔗 **[Try it on Google Colab](<https://colab.research.google.com/drive/17VTr89QegjvgTTx4a_doLZXAs6Bn_mQb?usp=sharing>)**  
> Download the notebook and execute cell by cell to run everything in one place — including BERT + Phi-2 + GPT!

---

### 🛠️ Local Setup Instructions

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/bert-gpt-chatbot.git
cd bert-gpt-chatbot
```

## 2. Install Dependencies

```
python -m venv venv
source venv/bin/activate  # or`venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

## 3.Download the Phi-2 Model Locally (Once)
   Requires ~5 Gb free disk space
```
# In a Python script or Jupyter cell
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="microsoft/phi-2",
    local_dir="models/phi-2",
    local_dir_use_symlinks=False
)
```

Or download manually and place contents in models/phi-2.

🔑 OpenAI API Key
If using GPT-3.5/4, input your OpenAI API key in the sidebar securely. Your key is not stored.

📌 Note About Google Colab
If you want to run the entire project in Google Colab, we’ve prepared a single notebook for that.

📎 **[Open in Colab](<notebook/implement_with_colab.ipynb>)**
Download the notebook and execute each cell to:

Download the Phi-2 model

Load the BERT model

Start Streamlit UI

Test chatbot responses

📜 License
MIT License © 2025 [kalyan]

