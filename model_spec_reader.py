###
#
# SAI Model Spec Reader
#
# Description:
# Provides functionalities for reading and displaying model metadata.

# License: Apache License, Version 2.0
#
###

import safetensors
import argparse
import toml
import os
import json
from io import BytesIO
import base64

# ==================
# UTILITY FUNCTIONS
# ==================

def has_metadata(model_path: str) -> bool:
    if not model_path.endswith(".safetensors"):
        return False
    
    with safetensors.safe_open(model_path, framework="pt") as f:
        metadata = f.metadata()
        
    return bool(metadata)


def load_metadata_from_safetensors(model_path: str) -> dict:
    if not model_path.endswith(".safetensors"):
        return {}
    
    with safetensors.safe_open(model_path, framework="pt") as f:
        metadata = f.metadata()

    return metadata if metadata else {}


def save_thumbnail(base64_data: str, filename: str):
    prefix, encoded = base64_data.split(",", 1)
    image_format = prefix.split("/")[1].split(";")[0]
    
    with open(f"{filename}.{image_format}", "wb") as f:
        f.write(base64.b64decode(encoded))


def display_metadata(model_path: str, only_sai: bool, save_metadata: str, save_thumbnail_flag: bool):
    model_name = os.path.splitext(os.path.basename(model_path))[0]
    print(f"\nMetadata for the model: {model_name}\n")
    
    metadata = load_metadata_from_safetensors(model_path)

    if only_sai:
        metadata = {k: v for k, v in metadata.items() if k.startswith('modelspec.')}

    output_str = ""
    if metadata:
        for key, value in metadata.items():
            output_str += f"{key:<30} {value}\n"
        print(output_str)
    else:
        print("Model does not have metadata.")
    
    if save_metadata:
        save_path = f"{model_name}.{save_metadata}"
        if save_metadata == "toml":
            with open(save_path, "w") as f:
                f.write(toml.dumps(metadata))
        else:  # Default to JSON
            with open(save_path, "w") as f:
                json.dump(metadata, f, indent=4)
        print(f"\nMetadata saved to: {save_path}")

    if save_thumbnail_flag and "modelspec.thumbnail" in metadata:
        save_thumbnail(metadata["modelspec.thumbnail"], model_name)
        print(f"\nThumbnail saved as: {model_name}.jpeg (or appropriate extension)")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Read and display metadata from a given model file.")
    parser.add_argument("--model_path", type=str, default="/content/model.safetensors", help="Path to the model file.")
    parser.add_argument("--only_sai", action="store_true", help="Only display SAI specific metadata.")
    parser.add_argument("--save_metadata", type=str, choices=["json", "toml"], help="Format to save the metadata. Choices are json and toml.")
    parser.add_argument("--save_thumbnail", action="store_true", help="Save the model thumbnail if available.")
    return parser.parse_args()


def main():
    args = parse_arguments()
    display_metadata(args.model_path, args.only_sai, args.save_metadata, args.save_thumbnail)
    

if __name__ == "__main__":
    main()
