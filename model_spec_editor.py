
###
#
# SAI Model Spec editor
#
# Description:
# Provides functionalities for managing and generating model metadata.
#
# References:
# Original Source: https://github.com/kohya-ss/sd-scripts/blob/dev/library/sai_model_spec.py
# Documentation: https://github.com/Stability-AI/ModelSpec
#
# License: Apache License, Version 2.0
#
###

import argparse
import base64
import datetime
import hashlib
import json
import os
import time
from io import BytesIO
from typing import List, Optional, Tuple, Union

from PIL import Image
import safetensors
from safetensors.torch import load_file, save_file

# ==================
# CONSTANTS
# ==================

BASE_METADATA = {
    "modelspec.sai_model_spec": "1.0.0",
    "modelspec.architecture": None,
    "modelspec.implementation": None,
    "modelspec.title": None,
    "modelspec.usage_hint": None,
    "modelspec.trigger_phrase": None,
    "modelspec.thumbnail": None,
    "modelspec.resolution": None,
    "modelspec.description": None,
    "modelspec.author": None,
    "modelspec.date": None,
    "modelspec.license": None,
    "modelspec.tags": None,
    "modelspec.merged_from": None,
    "modelspec.prediction_type": None,
    "modelspec.timestep_range": None,
    "modelspec.encoder_layer": None,
}

ARCHITECTURES = {
    "sd_v1": "stable-diffusion-v1",
    "sd_v2_512": "stable-diffusion-v2-512",
    "sd_v2_768_v": "stable-diffusion-v2-768-v",
    "sd_xl_v1_base": "stable-diffusion-xl-v1-base"
}

ADAPTERS = {
    "lora": "lora",
    "textual_inversion": "textual-inversion"
}

IMPLEMENTATIONS = {
    "stability_ai": "https://github.com/Stability-AI/generative-models",
    "diffusers": "diffusers"
}

PREDICTION_TYPES = {
    "epsilon": "epsilon",
    "v": "v"
}

# ==================
# UTILITY FUNCTIONS
# ==================

def load_bytes_in_safetensors(tensors):
    byte_data = safetensors.torch.save(tensors)
    byte_buffer = BytesIO(byte_data)
    byte_buffer.seek(8)
    n = int.from_bytes(byte_buffer.read(8), "little")
    byte_buffer.seek(n + 8)
    return byte_buffer.read()


def precalculate_safetensors_hashes(state_dict):
    hash_sha256 = hashlib.sha256()
    for tensor in state_dict.values():
        single_tensor_sd = {"tensor": tensor}
        bytes_for_tensor = load_bytes_in_safetensors(single_tensor_sd)
        hash_sha256.update(bytes_for_tensor)
    return f"0x{hash_sha256.hexdigest()}"


def update_hash_sha256(metadata: dict, state_dict: dict) -> str:
    metadata_str = json.dumps(metadata, sort_keys=True)
    state_dict_hash = precalculate_safetensors_hashes(state_dict)
    combined_str = metadata_str + state_dict_hash

    hash_sha256 = hashlib.sha256()
    hash_sha256.update(combined_str.encode('utf-8'))

    return f"0x{hash_sha256.hexdigest()}"


def image_to_base64(img_path: str) -> str:
    with Image.open(img_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
    return "data:image/jpeg;base64," + img_str.decode('utf-8')


def build_metadata(state_dict: Optional[dict], **kwargs) -> dict:
    metadata = BASE_METADATA.copy()

    arch = ARCHITECTURES.get(kwargs.get("architecture"))
    adapter = ADAPTERS.get(kwargs.get("adapter"))
    if adapter:
        arch += f"/{adapter}"
    metadata["modelspec.architecture"] = arch

    impl_key = kwargs.get("implementation") or ("stability_ai" if kwargs.get("is_stable_diffusion_ckpt", True) else "diffusers")
    metadata["modelspec.implementation"] = IMPLEMENTATIONS[impl_key]


    title = kwargs.get("title", "Checkpoint")
    metadata["modelspec.title"] = title if title else f"{adapter}@{kwargs.get('timestamp')}"

    direct_fields = ["author", "description", "license", "tags", "merged_from", "usage_hint", "trigger_phrase"]
    for field in direct_fields:
        if kwargs.get(field):
            metadata[f"modelspec.{field}"] = kwargs[field]

    thumbnail_path = kwargs.get("thumbnail")
    if thumbnail_path:
        thumbnail_base64 = image_to_base64(thumbnail_path)
        metadata["modelspec.thumbnail"] = thumbnail_base64

    timestamp_input = kwargs.get("timestamp")
    if timestamp_input:
        try:
            int_ts = int(timestamp_input)
        except ValueError:
            date_obj = datetime.datetime.strptime(timestamp_input, "%Y-%m-%d")
            int_ts = int(date_obj.timestamp())
    else:
        int_ts = int(time.time())

    date = datetime.datetime.fromtimestamp(int_ts).isoformat()
    metadata["modelspec.date"] = date

    reso = kwargs.get("reso")
    if reso:
        if isinstance(reso, str):
            reso = tuple(map(int, reso.split(",")))
        if len(reso) == 1:
            reso = (reso[0], reso[0])
        metadata["modelspec.resolution"] = f"{reso[0]}x{reso[1]}"

    metadata["modelspec.prediction_type"] = PREDICTION_TYPES[kwargs.get("prediction_type", "epsilon")]

    timesteps = kwargs.get("timesteps")
    if timesteps:
        if isinstance(timesteps, (str, int)):
            timesteps = (timesteps, timesteps)
        metadata["modelspec.timestep_range"] = f"{timesteps[0]},{timesteps[1]}"

    clip_skip = kwargs.get("clip_skip")
    if clip_skip is not None:
        metadata["modelspec.encoder_layer"] = f"{clip_skip}"

    metadata = {k: v for k, v in metadata.items() if v is not None}

    return metadata


def load_metadata_from_safetensors(model: str) -> dict:
    if not model.endswith(".safetensors"):
        return {}
    with safetensors.safe_open(model, framework="pt") as f:
        metadata = f.metadata()
    return metadata if metadata else {}


def initialize_and_process_metadata(args):
    print("Initializing metadata builder...")

    if args.timestamp is None:
        args.timestamp = time.time()

    print(f"Loading checkpoint from: {args.ckpt}...")
    state_dict = load_file(args.ckpt)
    print("Checkpoint loaded successfully.")

    existing_metadata = load_metadata_from_safetensors(args.ckpt)
    if existing_metadata:
        print("Existing metadata found in model.")

    metadata_args = {
        "implementation": args.implementation,
        "architecture": args.architecture,
        "adapter": args.adapter,
        "title": args.title,
        "description": args.description,
        "author": args.author,
        "license": args.license,
        "tags": args.tags,
        "usage_hint": args.usage_hint,
        "trigger_phrase": args.trigger_phrase,
        "thumbnail": args.thumbnail,
        "merged_from": args.merged_from,
        "prediction_type": args.prediction_type,
        "reso": args.reso,
        "timesteps": args.timesteps,
        "clip_skip": args.clip_skip,
        "timestamp": args.timestamp
    }
    new_metadata = build_metadata(state_dict, **metadata_args)

    for key, value in new_metadata.items():
        existing_metadata[key] = value

    metadata = existing_metadata

    print("Metadata built successfully.")
    print(metadata)

    if args.add_hash:
        print("Calculating hash for metadata...")
        metadata["modelspec.hash_sha256"] = update_hash_sha256(metadata, state_dict)
        print("Hash added to metadata.")

    if args.debug:
        print("Debug mode activated. Displaying metadata:")
        print(json.dumps(metadata, indent=4))
    else:
        print(f"Saving model with metadata to: {args.output_file}...")
        from safetensors.torch import save_file
        save_file(state_dict, args.output_file, metadata)
        print("Model saved successfully.")

    print("Metadata builder completed.")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Metadata input for model.")
    parser.add_argument("--ckpt", type=str, required=True, help="Path to checkpoint file.")
    parser.add_argument("--implementation", type=str, choices=list(IMPLEMENTATIONS.keys()), default=None, help="Implementation source of the model.")
    parser.add_argument("--architecture", type=str, choices=list(ARCHITECTURES.keys()), default="sd_v1", help="Model architecture.")
    parser.add_argument("--adapter", type=str, choices=list(ADAPTERS.keys()), default=None, help="Adapter type.")
    parser.add_argument("--title", type=str, default=None, help="Title of the model.")
    parser.add_argument("--description", type=str, default=None, help="Description of the model.")
    parser.add_argument("--author", type=str, default=None, help="Author of the model.")
    parser.add_argument("--license", type=str, default=None, help="License for the model.")
    parser.add_argument("--tags", type=str, default=None, help="Tags for the model.")
    parser.add_argument("--usage_hint", type=str, default=None, help="Usage hints for the model.")
    parser.add_argument("--trigger_phrase", type=str, default=None, help="Trigger phrases for the model, separated by commas.")
    parser.add_argument("--thumbnail", type=str, default=None, help="Path to the thumbnail image for the model.")
    parser.add_argument("--merged_from", type=str, default=None, help="Models merged from.")
    parser.add_argument("--prediction_type", type=str, choices=list(PREDICTION_TYPES.keys()), default="epsilon", help="Prediction type for the model.")
    parser.add_argument("--reso", type=str, default=None, help="Resolution of the model.")
    parser.add_argument("--timesteps", type=str, default=None, help="Timesteps for the model.")
    parser.add_argument("--clip_skip", type=int, default=None, help="Encoder layer clip skip.")
    parser.add_argument("--timestamp", type=str, default=None, help="Timestamp for the model. If not provided, current time is used.")
    parser.add_argument("--output_file", type=str, default="model.safetensors", help="Output file location.")
    parser.add_argument("--debug", action="store_true", help="If set, only print the metadata and don't save.")
    parser.add_argument("--add_hash", action="store_true", help="If set, add a hash to the metadata.")

    return parser.parse_args()


def main():
    args = parse_arguments()
    initialize_and_process_metadata(args)
    
    
if __name__ == "__main__":
    main()    
