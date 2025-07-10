import tkinter as tk
from tkinter import scrolledtext
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re

def get_response(user_input):
    user_input = user_input.lower().strip()
    # Predefined responses
    if user_input == "hello":
        return "Hi!"
    elif user_input == "how are you":
        return "I'm fine, thanks!"
    elif user_input == "bye":
        return "Goodbye!"
    else:
        # Check for weather-related query
        if "weather" in user_input or "wheather" in user_input:
            # Extract location (basic approach: assume words after "weather"/"wheather")
            words = user_input.split()
            location = " ".join(words[words.index("weather") + 1:] if "weather" in words else words[words.index("wheather") + 1:] if "wheather" in words else [])
            if not location:
                return "Please specify a city for the weather (e.g., 'weather in New York')."
            search_query = f"current weather in {location}"
        else:
            search_query = user_input

        # Perform web search
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}  # Mimic browser to avoid blocks
            for url in search(search_query, num_results=3):
                try:
                    # Fetch page content
                    response = requests.get(url, headers=headers, timeout=5)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for weather-specific data (temperature, conditions)
                    if "weather" in search_query:
                        # Target common weather elements (e.g., temperature, conditions)
                        temp_elements = soup.find_all(['span', 'div'], string=re.compile(r'\d+[°CF]'))
                        for elem in temp_elements:
                            text = elem.get_text().strip()
                            if text and len(text) < 50:  # Short text likely contains temp/conditions
                                return text[:150] + "..." if len(text) > 150 else text
                        # Try paragraphs or meta descriptions for conditions
                        paragraphs = soup.find_all('p')
                        for p in paragraphs:
                            text = p.get_text().strip()
                            if any(keyword in text.lower() for keyword in ['sunny', 'cloudy', 'rain', 'snow', 'temperature']):
                                return text[:150] + "..." if len(text) > 150 else text
                    # General search for non-weather queries
                    meta = soup.find('meta', attrs={'name': 'description'})
                    if meta and meta.get('content'):
                        return meta.get('content')[:150] + "..." if len(meta.get('content')) > 150 else meta.get('content')
                    for p in soup.find_all('p'):
                        text = p.get_text().strip()
                        if text and len(text) > 50:
                            return text[:150] + "..." if len(text) > 150 else text
                except Exception:
                    continue  # Try next URL if current one fails
            return "No clear answer found. Try rephrasing or specifying a city."
        except Exception:
            return "Search failed. Try again!"

def send_message():
    user_input = entry.get()
    if user_input:
        chat_area.config(state='normal')
        chat_area.insert(tk.END, "You: " + user_input + "\n")
        response = get_response(user_input)
        chat_area.insert(tk.END, "Bot: " + response + "\n\n")
        chat_area.config(state='disabled')
        entry.delete(0, tk.END)
        chat_area.yview(tk.END)

def send_message_event(event):
    send_message()

# Create the main window
root = tk.Tk()
root.title("Chatbot with Weather Search")
root.geometry("400x500")

# Create and configure the chat display area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', height=20)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create and configure the input entry field
entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=5, fill=tk.X)
entry.bind("<Return>", send_message_event)

# Create and configure the send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=5)

# Start the main loop
root.mainloop()