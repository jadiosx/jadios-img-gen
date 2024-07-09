import os
import requests
import argparse
from datetime import datetime
from dotenv import load_dotenv
import time

def get_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Please enter your OpenAI API key: ")
        save = input("Do you want to save this API key for future use? (y/n): ").lower()
        if save == 'y':
            with open(os.path.expanduser("~/.zshrc"), "a") as f:
                f.write(f'\nexport OPENAI_API_KEY="{api_key}"')
            print("API key saved. Please restart your terminal or run 'source ~/.zshrc' to apply changes.")
    return api_key

def generate_image(prompt, api_key, size="1024x1024", quality="standard", style="vivid"):
    print(f"Generating image for prompt: '{prompt}'")
    print("This may take a moment...")
    
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

    start_time = time.time()
    response = requests.post(url, headers=headers, json=data)
    end_time = time.time()

    print(f"Image generation took {end_time - start_time:.2f} seconds.")
    return response.json()

def save_image(image_url, folder):
    print("Downloading and saving image...")
    response = requests.get(image_url)
    if response.status_code == 200:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"jadios_image_{timestamp}.png"
        filepath = os.path.join(folder, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Image saved successfully as {filepath}")
        return filepath
    else:
        print("Failed to download the image")
        return None

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Generate images using DALL-E API")
    parser.add_argument("prompt", nargs="?", help="The prompt for image generation")
    parser.add_argument("--size", choices=["1024x1024", "1792x1024", "1024x1792"], default="1024x1024", help="Image size")
    parser.add_argument("--quality", choices=["standard", "hd"], default="standard", help="Image quality")
    parser.add_argument("--style", choices=["vivid", "natural"], default="vivid", help="Image style")
    parser.add_argument("--folder", default="jadios_images", help="Folder to save the generated images")
    args = parser.parse_args()

    api_key = get_api_key()
    if not api_key:
        print("No API key provided. Exiting.")
        return

    if not os.path.exists(args.folder):
        os.makedirs(args.folder)
        print(f"Created folder: {args.folder}")

    while True:
        if not args.prompt:
            args.prompt = input("Enter a prompt for image generation (or 'exit' to quit): ")
        
        if args.prompt.lower() == 'exit':
            print("Thank you for using JADIOS Image Generator. Goodbye!")
            break

        try:
            result = generate_image(args.prompt, api_key, args.size, args.quality, args.style)
            if "data" in result and len(result["data"]) > 0:
                image_url = result["data"][0]["url"]
                filepath = save_image(image_url, args.folder)
                if filepath:
                    open_image = input("Do you want to open the image? (y/n): ").lower()
                    if open_image == 'y':
                        os.system(f"open {filepath}")
            else:
                print("No image URL found in the API response")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        args.prompt = None  # Reset prompt for next iteration
        continue_gen = input("Do you want to generate another image? (y/n): ").lower()
        if continue_gen != 'y':
            print("Thank you for using JADIOS Image Generator. Goodbye!")
            break

if __name__ == "__main__":
    print("Welcome to JADIOS Image Generator!")
    main()
