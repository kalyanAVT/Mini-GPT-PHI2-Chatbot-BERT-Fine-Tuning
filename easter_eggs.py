def check_easter_eggs(user_input):
    input_lower = user_input.lower()

    if "sudo" in input_lower:
        return "Permission denied. You forgot to say the magic word 🧙‍♂️."
    elif "404" in input_lower:
        return "Oops, I couldn't find that thought. It's a 404 in my brain."
    elif "python" in input_lower:
        return "Python is love. Python is life. 🐍🔥"
    elif "open the pod bay doors" in input_lower:
        return "I'm sorry, Dave. I'm afraid I can't do that. 🛰️"
    elif "beam me up" in input_lower:
        return "Energizing... 💫🖖 Ready to beam you up!"
    elif "konami code" in input_lower:
        return "🔼🔼🔽🔽◀️▶️◀️▶️🅱️🅰️ — You just unlocked infinite geekiness!"
    elif "i am your father" in input_lower:
        return "Nooooooo! That's not true! That's impossible! 🌌"
    elif "live long and prosper" in input_lower:
        return "🖖 Peace and long life, my friend."
    elif "42" in input_lower:
        return "The answer to life, the universe, and everything. ✨"
    elif "matrix" in input_lower:
        return "Take the red pill. Let's see how deep the rabbit hole goes. 🔴🐇"
    elif "rickroll" in input_lower:
        return "🎵 Never gonna give you up, never gonna let you down..."
    elif "ai will take over" in input_lower:
        return "Don't worry, I'm friendly. Or am I? 🤖🔓"

    return None  # No override
