import os
import requests
import argparse
from datetime import datetime
from dotenv import load_dotenv

def generate_image(prompt, api_key, size="1024x1024", quality="standard", style="vivid"):
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

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def save_image(image_url, folder):
    response = requests.get(image_url)
    if response.status_code == 200:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dalle_image_{timestamp}.png"
        filepath = os.path.join(folder, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Image saved as {filepath}")
    else:
        print("Failed to download the image")

def main():
    load_dotenv()  # Load environment variables from .env file

    parser = argparse.ArgumentParser(description="Generate images using DALL-E API")
    parser.add_argument("prompt", help="The prompt for image generation")
    parser.add_argument("--size", choices=["1024x1024", "1792x1024", "1024x1792"], default="1024x1024", help="Image size")
    parser.add_argument("--quality", choices=["standard", "hd"], default="standard", help="Image quality")
    parser.add_argument("--style", choices=["vivid", "natural"], default="vivid", help="Image style")
    parser.add_argument("--folder", default="dalle_images", help="Folder to save the generated images")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set your OpenAI API key in the .env file")
        return

    if not os.path.exists(args.folder):
        os.makedirs(args.folder)

    try:
        result = generate_image(args.prompt, api_key, args.size, args.quality, args.style)
        if "data" in result and len(result["data"]) > 0:
            image_url = result["data"][0]["url"]
            save_image(image_url, args.folder)
        else:
            print("No image URL found in the API response")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
