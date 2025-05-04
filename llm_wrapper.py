from transformers import AutoTokenizer, AutoModelForCausalLM
from sentiment import predict_sentiment
import torch

# Load phi-2 locally from custom directory
PHI2_PATH = "models/phi-2"

class LocalLLMResponder:
    def __init__(self, model_path: str = PHI2_PATH):
        print("🔍 Loading Phi-2 model from local path...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        self.model.eval()
        if torch.cuda.is_available():
            self.model.to("cuda")
        elif torch.backends.mps.is_available():
            self.model.to("mps")
        else:
            self.model.to("cpu")
        print("✅ Phi-2 loaded successfully!")

    def generate_response(self, user_message):
        sentiment = predict_sentiment(user_message)["label"]
        prompt = self.build_prompt(user_message, sentiment)

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        if torch.cuda.is_available():
            inputs = {k: v.to("cuda") for k, v in inputs.items()}
        elif torch.backends.mps.is_available():
            inputs = {k: v.to("mps") for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=150, temperature=0.7)
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Remove prompt from response (extract only reply)
        reply = response.replace(prompt, "").strip()
        return reply, "phi-2"

    def build_prompt(self, message, sentiment):
        tone_instruction = {
            "Positive": "Respond helpfully with excitement and optimism.",
            "Negative": "Respond with empathy and encouragement.",
            "Neutral": "Respond in a balanced and informative way."
        }

        prompt = f"""You are a friendly and intelligent AI assistant.
Sentiment of the user's message: {sentiment}.
{tone_instruction[sentiment]}
User: {message}
Assistant:"""

        return prompt
