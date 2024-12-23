# TagSorter

A simple command-line tool for organizing images based on AI-detected tags.

## Features

- Fast and accurate image tagging using AI
- Batch processing of images
- Copy/Move/Delete files based on detected tags
- Interactive command-line interface

## Installation

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Simply run:
```bash
python run.py
```

The program will guide you through:
1. Selecting source folder
2. Choosing operation (copy/move/delete)
3. Setting destination folder (if needed)
4. Entering tags to search for

## Model

Uses advanced AI model that provides:
- High accuracy tag detection
- Fast processing
- Wide range of recognizable tags

## GPU Support

For GPU acceleration, install CUDA support:
```bash
pip install onnxruntime-gpu
```

## Credits

Based on [stable-diffusion-webui-wd14-tagger](https://github.com/picobyte/stable-diffusion-webui-wd14-tagger)