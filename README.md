# JADIOS Image Generator

JADIOS Image Generator is a Python script that utilizes the DALL-E API to generate images based on text prompts. It provides a user-friendly command-line interface for creating AI-generated images with various customization options.

## Features

- Generate images using text prompts
- Customize image size, quality, and style
- Save generated images to a specified folder
- Interactive mode for multiple image generations
- Loading animation during image generation
- Option to automatically open generated images

## Requirements

- Python 3.6 or higher
- OpenAI API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/jadios-image-generator.git
   cd jadios-image-generator
   ```

2. Install the required packages:
   ```
   pip3 install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project directory
   - Add your API key to the file:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Usage

Run the script using Python 3:

```
python3 jadios_img_gen.py [prompt] [options]
```

### Options:

- `prompt`: The text prompt for image generation (optional, can be entered interactively)
- `--size`: Image size (1024x1024, 1792x1024, 1024x1792)
- `--quality`: Image quality (standard, hd)
- `--style`: Image style (vivid, natural)
- `--folder`: Folder to save generated images

### Examples:

1. Generate an image interactively:
   ```
   python3 jadios_img_gen.py
   ```

2. Generate an image with a prompt:
   ```
   python3 jadios_img_gen.py "A futuristic cityscape at night"
   ```

3. Generate an image with custom options:
   ```
   python3 jadios_img_gen.py "A serene lake at sunset" --size 1792x1024 --quality hd --style natural
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
