def check_easter_eggs(user_input):
    input_lower = user_input.lower()
    
    if "sudo" in input_lower:
        return "Permission denied. You forgot to say the magic word 🧙‍♂️."
    elif "404" in input_lower:
        return "Oops, I couldn't find that thought. It's a 404 in my brain."
    elif "python" in input_lower:
        return "Python is love. Python is life. 🐍🔥"
    
    return None  # No override
