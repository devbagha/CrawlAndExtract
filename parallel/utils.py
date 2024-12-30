import re

def extract_emails(text):
    """Extract and return a list of emails from the given text."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)
