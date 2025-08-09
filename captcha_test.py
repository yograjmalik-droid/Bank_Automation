import random
def generate_captcha():
    a=str(random.randint(0, 9))               # Random digit (0-9)
    b=chr(random.randint(65, 80))             # Random uppercase letter (A-P)
    c=str(random.randint(0, 9))               # Another random digit
    d=chr(random.randint(97, 122))            # Random lowercase letter (a-z)
    captcha=f"{a} {b} {c} {d}"                # Formatted string with spaces
    return captcha
