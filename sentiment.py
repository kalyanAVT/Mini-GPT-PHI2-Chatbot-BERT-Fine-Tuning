import torch
from transformers import BertTokenizer, BertForSequenceClassification
import sys
import os
sys.path.append(os.path.abspath('..')) # Adjust the path to your project structure
# Load fine-tuned model and tokenizer
model_path = os.path.abspath("model/bert_sentiment_model")  # or your final checkpoint path
tokenizer = BertTokenizer.from_pretrained(model_path, local_files_only=True)
model = BertForSequenceClassification.from_pretrained(model_path, local_files_only=True)
model.eval()

# Move to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define labels — update as per your fine-tuning
label_map = {
    0: "Negative",
    1: "Neutral",
    2: "Positive"
}

def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    inputs = {key: val.to(device) for key, val in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=-1)
        pred = torch.argmax(probs, dim=1).item()

    return {
        "text": text,
        "label": label_map[pred],
        "confidence": round(probs[0][pred].item(), 4)
    }

# Example usage
if __name__ == "__main__":
    while True:
        user_input = input("Enter a sentence (or 'q' to quit): ")
        if user_input.lower() == 'q':
            break
        result = predict_sentiment(user_input)
        print(f"Sentiment: {result['label']} (Confidence: {result['confidence']})\n")
