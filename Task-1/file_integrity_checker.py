import hashlib
import os
import json

def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def save_hashes(folder_path, output_file="hashes.json"):
    hashes = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            path = os.path.join(root, file)
            hashes[path] = calculate_hash(path)
    with open(output_file, "w") as f:
        json.dump(hashes, f, indent=2)

def verify_integrity(folder_path, original_hash_file="hashes.json"):
    with open(original_hash_file, "r") as f:
        old_hashes = json.load(f)
    for path, old_hash in old_hashes.items():
        if not os.path.exists(path):
            print(f"[MISSING] {path}")
        elif calculate_hash(path) != old_hash:
            print(f"[MODIFIED] {path}")
        else:
            print(f"[OK] {path}")

