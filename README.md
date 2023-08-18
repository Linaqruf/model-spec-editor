
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

The main script can be run via the command line. Here's how to use it:

```bash
python model_spec_editor.py --ckpt "Anything-XL.safetensors" --title "Sample Model" --author "John Doe"

```

#### Options:

- `--ckpt`: Checkpoint for the model.
- `--architecture`: The architecture type.
- `--implementation`: Implementation type.
- `--adapter`: Adapter type.
- `--title`: Title of the model.
- `--description`: Description of the model.
- `--author`: Author of the model.
- `--license`: License for the model.
- `--tags`: Tags for the model.
- `--usage_hint`: Usage hints for the model.
- `--trigger_phrase`: Trigger phrases for the model, separated by commas.
- `--thumbnail`: Path to the thumbnail image for the model.
- `--merged_from`: Models merged from.
- `--prediction_type`: Prediction type for the model.
- `--reso`: Resolution of the model.
- `--timesteps`: Timesteps for the model.
- `--clip_skip`: Encoder layer clip skip.
- `--timestamp`: Timestamp for the model. If not provided, the current time is used.
- `--output_file`: Output file location.
- `--debug`: If set, only print the metadata and don't save.
- `--add_hash`: If set, add a hash to the metadata.

## References

- Original Source: [https://github.com/kohya-ss/sd-scripts/blob/dev/library/sai_model_spec.py](https://github.com/kohya-ss/sd-scripts/blob/dev/library/sai_model_spec.py)
- Documentation: [https://github.com/Stability-AI/ModelSpec](https://github.com/Stability-AI/ModelSpec)

## License

This project is licensed under the Apache License, Version 2.0. See the `LICENSE` file for details.
