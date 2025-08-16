import hashlib
import os
import json

HASH_FILE = "file_hashes.json"

def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def scan_directory(directory):
    hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            hashes[path] = hash_file(path)
    return hashes

def save_hashes(hashes):
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f, indent=4)

def load_hashes():
    if not os.path.exists(HASH_FILE):
        return {}
    with open(HASH_FILE, "r") as f:
        return json.load(f)

def compare_hashes(old, new):
    for path, h in new.items():
        if path not in old:
            print(f"[NEW] {path}")
        elif old[path] != h:
            print(f"[MODIFIED] {path}")
    for path in old:
        if path not in new:
            print(f"[DELETED] {path}")

if __name__ == "__main__":
    directory = input("Enter directory to scan: ").strip()
    new_hashes = scan_directory(directory)
    old_hashes = load_hashes()
    compare_hashes(old_hashes, new_hashes)
    save_hashes(new_hashes)
    print("Scan complete. Hashes updated.")
