import json
import os
import hashlib

def sha256_file(path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def scan_folder(folder_path):
    """
    Scans a folder, extracts text from files, and detects duplicates.

    Args:
        folder_path (str): The path to the folder to scan.

    Returns:
        str: A JSON string with the scan results.
    """
    results = {
        "files": [],
        "duplicates": {},
        "folder_signatures": []
    }

    seen_hashes = {}

    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            full_path = os.path.normpath(os.path.join(root, filename))
            file_hash = sha256_file(full_path)
            
            if not file_hash:
                continue
                
            file_size = os.path.getsize(full_path)
            content = ""
            
            # Basic text extraction for common text formats
            if filename.lower().endswith(('.txt', '.md', '.py', '.json', '.html', '.css', '.js')):
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                except Exception:
                    pass

            file_entry = {
                "path": full_path,
                "text": content,
                "size_bytes": file_size,
                "hash": file_hash,
                "metadata": {}
            }
            results["files"].append(file_entry)

            if file_hash in seen_hashes:
                if file_hash not in results["duplicates"]:
                    results["duplicates"][file_hash] = [seen_hashes[file_hash]]
                results["duplicates"][file_hash].append(full_path)
            else:
                seen_hashes[file_hash] = full_path

    return json.dumps(results, indent=2)

if __name__ == '__main__':
    # Example usage:
    # Replace 'your_folder_path' with the actual folder path you want to scan.
    folder_to_scan = 'your_folder_path' 
    if os.path.exists(folder_to_scan):
        scan_results = scan_folder(folder_to_scan)
        print(scan_results)
    else:
        print(f"Folder not found: {folder_to_scan}")
