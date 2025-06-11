import os
import requests
import argparse
from bs4 import BeautifulSoup
from subprocess import run

# Default collection URL (can be overridden)
DEFAULT_COLLECTION_URL = "https://huggingface.co/collections/common-pile/common-pile-v01-raw-data-6826b454a5a6a445d0b51b37"
CLONE_DIR = "hf_dataset_repos"

def get_collection_url():
    """Get collection URL from environment variable, command line args, or user input."""
    parser = argparse.ArgumentParser(description="Git clone datasets from a Hugging Face collection")
    parser.add_argument("--collection-url", "-c", 
                       help="URL of the Hugging Face collection to clone")
    parser.add_argument("--clone-dir", "-d", default=CLONE_DIR,
                       help=f"Directory to clone datasets to (default: {CLONE_DIR})")
    
    args = parser.parse_args()
    
    # Priority: command line arg > environment variable > user input > default
    collection_url = args.collection_url
    
    if not collection_url:
        collection_url = os.getenv("HF_COLLECTION_URL")
    
    if not collection_url:
        print("No collection URL provided.")
        collection_url = input(f"Enter Hugging Face collection URL (or press Enter for default): ").strip()
        
    if not collection_url:
        collection_url = DEFAULT_COLLECTION_URL
        print(f"Using default collection URL: {collection_url}")
    
    return collection_url, args.clone_dir

def get_dataset_ids(collection_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(collection_url, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.select("a[href^='/datasets/']")
    return list(set(link['href'].split("/datasets/")[1] for link in links))

def git_clone_datasets(dataset_ids, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    for dataset_id in dataset_ids:
        org, name = dataset_id.split("/")
        repo_url = f"https://huggingface.co/datasets/{org}/{name}"
        dest_path = os.path.join(target_dir, dataset_id.replace("/", "__"))
        if os.path.exists(dest_path):
            print(f"[SKIP] {dataset_id} already cloned.")
            continue
        print(f"[CLONE] {dataset_id}")
        run(["git", "clone", "--depth", "1", repo_url, dest_path], check=False)

if __name__ == "__main__":
    collection_url, clone_dir = get_collection_url()
    
    print(f"Collection URL: {collection_url}")
    print(f"Clone directory: {clone_dir}")
    
    ids = get_dataset_ids(collection_url)
    print(f"Found {len(ids)} dataset repos.")
    git_clone_datasets(ids, clone_dir)

