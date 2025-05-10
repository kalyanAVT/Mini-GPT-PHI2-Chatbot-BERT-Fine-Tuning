from transformers import AutoTokenizer, AutoModelForCausalLM
from sentiment import predict_sentiment
import torch
import requests
import json

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


class FlanT5Responder:
    def __init__(self, restapi_url):
        self.restapi_url = restapi_url

    def generate_response(self, question, context=""):
        sentiment = predict_sentiment(question)["label"]
        if not context:
            context = "This chat is to support the user, and you are friendly, taking care of the user. You are a helpful assistant."

        # Updated prompt format for FLAN-T5 instruction-following
        inputs_text = (
            f"Instruction: Answer the user's question in a friendly and helpful way.\n\n"
            f"User: {question}\n\n"
            f"Context: {context}"
        )

        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(self.restapi_url, json={"inputs": inputs_text}, headers=headers)
            response.raise_for_status()
            result = response.json()

            if isinstance(result, dict) and "body" in result:
                inner_body = json.loads(result["body"])
                answer_data = inner_body.get("answer", [])
                if isinstance(answer_data, list) and len(answer_data) > 0:
                    generated_text = answer_data[0].get("generated_text", "").strip()
                else:
                    generated_text = ""
            elif isinstance(result, list) and "generated_text" in result[0]:
                generated_text = result[0]["generated_text"].strip()
            else:
                generated_text = ""

            # Fallback if empty or echo
            if not generated_text or question.lower() in generated_text.lower():
                generated_text = "⚠️ No proper answer generated."

            return generated_text, "flan-t5"

        except requests.RequestException as e:
            return f"Error: Failed to reach API - {e}", "flan-t5"
        except Exception as e:
            return f"Error: {e}", "flan-t5"
