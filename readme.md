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
If you want to run the entire project in Google Colab, I’ve prepared a single notebook for that.(Note:- "This notebook does not contain any AWS SageMaker features or files.")

📎 **[Open in Colab](<notebook/implement_with_colab.ipynb>)**
Download the notebook and execute each cell to:

Download the Phi-2 model

Load the BERT model

Start Streamlit UI

Test chatbot responses

## New feature
now you can use APi Gateway of AWS to deploy and get response with this process:
🚀 How to Run MOdel in on AWS SageMaker

Hey there! 👋 Here's how you can run big Models of HuggingFace using AWS SageMaker + Lambda + API Gateway. Let’s get started:

📓 1. Launch JupyterLab in SageMaker
Go to your AWS SageMaker Console.

Create a Notebook instance (e.g., ml.m3.medium/ml.m5.xlarge) FreeTier.

After it’s ready, click Open JupyterLab.

Upload or clone this repo into the notebook instance. OR make a new file and paste each cell in it. Here this is the [notebook](<notebook/jupyterlab_file-for-sagemaker-instance.ipynb>)

🛠️ 2. Set Up the Lambda Function
In the AWS Lambda Console, create a new function.

Use the [lambda_function.py](<lambda_function.py>) from this repo.

Set the runtime to Python 3.x.

Make sure the function has permission to be invoked via API Gateway.

Change the EndPoint name in the file after Executing the jupyter notebook.

Then Deploy the Function.

🌐 3. Connect API Gateway
Go to API Gateway Console.

Create a REST API.

Add a resource like /invoke.

Add a POST method linked to your Lambda.

Deploy the API to a stage (e.g., prod).

Copy the Invoke URL, e.g.:
```bash
https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/invoke
```
🔑 4. Configure the .env File
Update the .env file in the root of this project:

```bash
LAMBDA_INVOKE_URL="https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/invoke"
```
✅ That’s It!
You're now ready to use this project with AWS services.
Run the app, interact with the chatbot, and trigger the Lambda using your SageMaker notebook!

📜 License
## License

This project does not currently have an open-source license. All rights are reserved by the author. Please contact the repository owner if you wish to use or contribute to this project.
[kalyan](<https://github.com/kalyanAVT>)

