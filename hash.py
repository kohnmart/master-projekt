import hashlib
import os

def hash_file(file_path):
    """Generate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def hash_folder(folder_path):
    """Hash all files in the folder and combine into a final hash."""
    sha256_hash = hashlib.sha256()
    for root, _, files in os.walk(folder_path):
        for file in sorted(files):  # Ensure consistent file order
            file_path = os.path.join(root, file)
            sha256_hash.update(hash_file(file_path).encode())
    return sha256_hash.hexdigest()

def save_hash_to_file(hash_value, output_file):
    """Save the hash value to a file."""
    with open(output_file, "w") as f:
        f.write(hash_value)

# Example usage
folder_path = "./"
final_hash = hash_folder(folder_path)

# Store the final hash in a file (e.g., hash_output.txt)
output_file = "./hash_output.txt"
save_hash_to_file(final_hash, output_file)

print(f"Final folder hash saved to {output_file}: {final_hash}")
