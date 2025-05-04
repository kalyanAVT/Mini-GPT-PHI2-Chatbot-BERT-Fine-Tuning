import os
from openai import OpenAI, RateLimitError, AuthenticationError, APIError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_gpt(user_message, style="normal"):
    """
    Chat with GPT-4o (fallback to GPT-3.5-turbo on error). 
    Responds in geeky or normal style.
    """
    system_prompt = (
        "You are a geeky, funny assistant who talks like a tech-savvy meme lord. Use light humor, coding jokes, and internet slang."
        if style == "techy"
        else "You are a friendly and helpful assistant who answers user questions clearly and politely."
    )

    try:
        # Try GPT-4o
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except RateLimitError:
        # Quota exceeded, fallback to GPT-3.5
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return "(Fallback to GPT-3.5) " + response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️ GPT fallback failed too: {e}"

    except AuthenticationError:
        return "🚫 API Key issue. Please check your OpenAI API key."

    except APIError as e:
        return f"⚠️ API Error: {e}"

    except Exception as e:
        return f"⚠️ Unexpected Error: {e}"
