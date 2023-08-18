
# Model Spec Editor

This repository provides functionalities for managing and generating model metadata, with a focus on the unofficial Stability.AI Model Metadata Standard Specification.

## Description

The `model_spec_editor.py` script aids in managing and generating model metadata. It offers a range of utilities to handle metadata tasks, from encoding images to generating hashes. This tool is essential for users looking to work with the Stability.AI Model Metadata Standard Specification.

### Key Features

- Generate and manage model metadata.
- Command-line interface for easy metadata editing.
- Save metadata to `.safetensors` model files.
- Built-in utilities for tasks like encoding images and generating hashes.

## Getting Started

### Prerequisites

Ensure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```

### Usage

Both of script can be run via the command line. Here's how to use it:

To write metadata, use `model_spec_editor.py`

```bash
python model_spec_editor.py \
    --ckpt "./amelia_watson_xl.safetensors" \
    --output_file "./amelia_watson_xl_mod.safetensors" \
    --add_hash \
    --implementation "stability_ai" \
    --architecture "sd_xl_v1_base" \
    --adapter "lora" \
    --title "Amelia Watson XL LoRA" \
    --description "Amelia Watson, a charismatic time-traveling detective from the virtual realm of Hololive. Dive into her universe with this model featuring all her iconic outfits and complementary accessories. Use the generic 'amelia watson' tag to cater to diverse scenarios and imaginative requirements." \
    --author "Linaqruf" \
    --license "CreativeML Open RAIL++-M License" \
    --tags "anime, character, waifu, hololive" \
    --usage_hint "Recommended strength 70% (0.7). Use with ComfyUI, Automatic1111 and Diffusers library as SDXL LoRA adapter." \
    --trigger_phrase "amelia watson, amelia_detective, amelia_casual, amelia_formal, amelia_kimono" \
    --thumbnail "./amelia_watson_xl_upscaled.png" \
    --prediction_type "epsilon" \
    --reso "1024,1024" \
    --timestamp "2023-08-18" 
```

To read metadata, use `model_spec_reader.py`

```bash
python model_spec.py --model_path /content/amelia_watson_xl_mod.safetensors --only_sai --save_metadata json --save_thumbnail
```

Result:
```bash
Metadata for the model: amelia_watson_xl_mod

modelspec.implementation       https://github.com/Stability-AI/generative-models
modelspec.sai_model_spec       1.0.0
modelspec.trigger_phrase       amelia watson, amelia_detective, amelia_casual, amelia_formal, amelia_kimono
modelspec.thumbnail            data:image/jpeg;base64xxxxxxxxxxxxxxxxxxxxxxxxxxxx
modelspec.usage_hint           Recommended strength 70% (0.7). Use with ComfyUI, Automatic1111 and Diffusers library as SDXL LoRA adapter.
modelspec.date                 2023-08-18T00:00:00
modelspec.hash_sha256          0x098c257abe19fb1b03500a6a6d443f52f6bf77ac00b6e005c2ef8c1bbd7de8a6
modelspec.author               Linaqruf
modelspec.prediction_type      epsilon
modelspec.title                Amelia Watson XL LoRA
modelspec.tags                 anime, character, waifu, hololive
modelspec.resolution           1024x1024
modelspec.description          Amelia Watson, a charismatic time-traveling detective from the virtual realm of Hololive. Dive into her universe with this model featuring all her iconic outfits and complementary accessories. Use the generic 'amelia watson' tag to cater to diverse scenarios and imaginative requirements.
modelspec.license              CreativeML Open RAIL++-M License
modelspec.architecture         stable-diffusion-xl-v1-base/lora

```

#### Options:
1. Model Spec Editor
- `--ckpt`: Checkpoint for the model.
- `--architecture`: The architecture type, choose between `sd_v1`, `sd_v2_512`, `sd_v2_768_v`, or `sd_xl_v1_base`
- `--implementation`: Implementation type, choose between `stability_ai` or `diffusers`.
- `--adapter`: Adapter type if the model is not the big one, choose between `lora` and `textual-inversion`.
- `--title`: Title of the model,
- `--description`: Description of the model.
- `--author`: Author of the model. 
- `--license`: License for the model, example: `CC-BY-SA-4.0` or `CreativeML Open RAIL-M`
- `--tags`: Tags for the model, example: `anime, character, vtuber`, or `realistic, scenery`
- `--usage_hint`: Usage hints for the model, example: `use with 0.7 weight`
- `--trigger_phrase`: Trigger phrases for the model, separated by commas, example: `use 'pixel' as a prompt to trigger the artstyle`
- `--thumbnail`: Path to the thumbnail image for the model.
- `--merged_from`: Models merged from. 
- `--prediction_type`: Prediction type for the model, normally it's `epsilon`.
- `--reso`: Resolution of the model, example: `1024,1024`
- `--timesteps`: Timesteps for the model, usage: `<min_timesteps>,<max_timesteps`
- `--clip_skip`: Encoder layer clip skip, example: `2`
- `--timestamp`: Timestamp for the model, example: `2023-08-18`. If not provided, the current time is used.
- `--output_file`: Output file location.
- `--debug`: If set, only print the metadata and don't save.
- `--add_hash`: If set, add a new hash to the metadata.

2. Model Spec Reader
- `--model_path`: Path to the `.safetensors` model file.
- `--only_sai`: Only display `SAI model spec`-specific metadata.
- `--save_metadata`: Format to save the metadata. Choices are `json` and `toml`.
- `--save_thumbnail`: Save the model thumbnail if available.

## References

- Original Source: [https://github.com/kohya-ss/sd-scripts/blob/dev/library/sai_model_spec.py](https://github.com/kohya-ss/sd-scripts/blob/dev/library/sai_model_spec.py)
- Documentation: [https://github.com/Stability-AI/ModelSpec](https://github.com/Stability-AI/ModelSpec)

## License

This project is licensed under the Apache License, Version 2.0. See the `LICENSE` file for details.
