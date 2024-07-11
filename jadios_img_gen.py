import os
import requests
import argparse
from datetime import datetime
from dotenv import load_dotenv
import time
import threading
import itertools
import sys
import random

def print_ascii_art():
    """Print ASCII art for the intro screen."""
    ascii_art = """
 ┬┌─┐┌┬┐┬┌─┐┌─┐  ┬┌┬┐┌─┐  ┌─┐┌─┐┌┐┌
 │├─┤ ││││ │└─┐  │││││ ┬  │ ┬├┤ │││
└┘┴ ┴─┴┘┴└─┘└─┘  ┴┴ ┴└─┘  └─┘└─┘┘└┘

    """
    print(ascii_art)
    print("JADIOS IMAGE GEN, where digital dreams become reality. 🌆🔮")

def spinning_cursor():
    """Generator for a spinning cursor animation."""
    while True:
        for cursor in '|/-\\':
            yield cursor

def loading_animation(stop_event, message):
    """Display a loading animation with a message in the terminal."""
    spinner = spinning_cursor()
    while not stop_event.is_set():
        sys.stdout.write(f"\r{message} {next(spinner)}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * (len(message) + 2) + '\r')
    sys.stdout.flush()

def get_api_key():
    """Retrieve or prompt for the OpenAI API key."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("🔑 API Key not found in environment variables.")
        api_key = input("Please enter your OpenAI API key: ")
        save = input("Do you want to save this API key for future use? (y/n): ").lower()
        if save == 'y':
            with open(os.path.expanduser("~/.zshrc"), "a") as f:
                f.write(f'\nexport OPENAI_API_KEY="{api_key}"')
            print("✅ API key saved. Please restart your terminal or run 'source ~/.zshrc' to apply changes.")
    return api_key

def generate_image(prompt, api_key, size="1024x1024", quality="standard", style="vivid"):
    """Generate an image using the DALL-E API."""
    print(f"\n🖼️  Generating image for prompt: '{prompt}'")
    print("🚀 Initializing DALL-E... Please wait...")
    
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": quality,
        "style": style
    }

    stop_event = threading.Event()
    loading_thread = threading.Thread(target=loading_animation, args=(stop_event, "🎨 Creating your masterpiece"))
    loading_thread.start()

    start_time = time.time()
    response = requests.post(url, headers=headers, json=data)
    end_time = time.time()

    stop_event.set()
    loading_thread.join()

    print(f"\n✨ Image generation completed in {end_time - start_time:.2f} seconds.")
    return response.json()

def save_image(image_url, folder):
    """Download and save the generated image."""
    print("📥 Downloading and saving image...")
    response = requests.get(image_url)
    if response.status_code == 200:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"jadios_image_{timestamp}.png"
        filepath = os.path.join(folder, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"✅ Image saved successfully as {filepath}")
        return filepath
    else:
        print("❌ Failed to download the image")
        return None

def print_random_fact():
    """Print a random fact about AI or art."""
    facts = [
        "Did you know? The term 'artificial intelligence' was coined in 1956 by John McCarthy.",
        "Fun fact: The first AI program, the Logic Theorist, was created in 1955 by Allen Newell and Herbert A. Simon.",
        "Art trivia: Leonardo da Vinci's Mona Lisa is considered the most famous painting in the world.",
        "AI fact: The Turing test, proposed by Alan Turing in 1950, is a test of a machine's ability to exhibit intelligent behavior.",
        "Art history: Vincent van Gogh only sold one painting during his lifetime.",
    ]
    print(f"\n🧠 {random.choice(facts)}")

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Generate images using DALL-E API (JADIOS Image Generator)")
    parser.add_argument("prompt", nargs="?", help="The prompt for image generation")
    parser.add_argument("--size", choices=["1024x1024", "1792x1024", "1024x1792"], default="1024x1024",
                        help="Image size (default: 1024x1024)")
    parser.add_argument("--quality", choices=["standard", "hd"], default="standard",
                        help="Image quality (default: standard)")
    parser.add_argument("--style", choices=["vivid", "natural"], default="vivid",
                        help="Image style (default: vivid)")
    parser.add_argument("--folder", default="jadios_images",
                        help="Folder to save the generated images (default: jadios_images)")
    args = parser.parse_args()

    print_ascii_art()

    api_key = get_api_key()
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return

    if not os.path.exists(args.folder):
        os.makedirs(args.folder)
        print(f"📁 Created folder: {args.folder}")

    while True:
        if not args.prompt:
            args.prompt = input("🖋️  Enter a prompt for image generation (or 'exit' to quit): ")
        
        if args.prompt.lower() == 'exit':
            print("👋 Thank you for using JADIOS Image Generator. Goodbye!")
            break

        try:
            result = generate_image(args.prompt, api_key, args.size, args.quality, args.style)
            if "data" in result and len(result["data"]) > 0:
                image_url = result["data"][0]["url"]
                filepath = save_image(image_url, args.folder)
                if filepath:
                    open_image = input("🖼️  Do you want to open the image? (y/n): ").lower()
                    if open_image == 'y':
                        os.system(f"open {filepath}")
            else:
                print("❌ No image URL found in the API response")
        except Exception as e:
            print(f"❌ An error occurred: {str(e)}")

        print_random_fact()

        args.prompt = None  # Reset prompt for next iteration
        continue_gen = input("🔄 Do you want to generate another image? (y/n): ").lower()
        if continue_gen != 'y':
            print("👋 Thank you for using JADIOS Image Generator. Goodbye!")
            break

if __name__ == "__main__":
    main()
