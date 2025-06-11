import os
import requests
import argparse
from bs4 import BeautifulSoup
from datasets import load_dataset
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Default collection URL (can be overridden)
DEFAULT_COLLECTION_URL = "https://huggingface.co/collections/common-pile/common-pile-v01-raw-data-6826b454a5a6a445d0b51b37"
SAVE_DIR = "downloaded_datasets"
MAX_WORKERS = 4  # Adjust based on your bandwidth & CPU
USE_AUTH_TOKEN = False # set to True if you need auth to access the dataset

def get_collection_url():
    """Get collection URL from environment variable, command line args, or user input."""
    parser = argparse.ArgumentParser(description="Download datasets from a Hugging Face collection")
    parser.add_argument("--collection-url", "-c", 
                       help="URL of the Hugging Face collection to download")
    parser.add_argument("--save-dir", "-s", default=SAVE_DIR,
                       help=f"Directory to save datasets (default: {SAVE_DIR})")
    parser.add_argument("--max-workers", "-w", type=int, default=MAX_WORKERS,
                       help=f"Maximum number of parallel downloads (default: {MAX_WORKERS})")
    
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
    
    return collection_url, args.save_dir, args.max_workers

def get_datasets_from_collection(collection_url):
    """Scrape dataset IDs from a Hugging Face collection page."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(collection_url, headers=headers)
    if not response.ok:
        raise Exception(f"Failed to fetch collection page: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    dataset_links = soup.select("a[href^='/datasets/']")
    dataset_ids = list(set(link["href"].split("/datasets/")[1] for link in dataset_links))
    return dataset_ids

def download_and_save_dataset(dataset_id, save_dir):
    """Download and save a single dataset locally."""
    local_path = os.path.join(save_dir, dataset_id.replace("/", "__"))
    if os.path.exists(local_path):
        return f"[SKIP] {dataset_id} already downloaded."

    try:
        dataset = load_dataset(dataset_id, use_auth_token=USE_AUTH_TOKEN)
        dataset.save_to_disk(local_path)
        return f"[OK] {dataset_id} saved to {local_path}"
    except Exception as e:
        return f"[FAIL] {dataset_id}: {e}"

def parallel_download(dataset_ids, save_dir, max_workers):
    os.makedirs(save_dir, exist_ok=True)
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_and_save_dataset, ds, save_dir): ds for ds in dataset_ids}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading"):
            result = future.result()
            results.append(result)
    return results

if __name__ == "__main__":
    collection_url, save_dir, max_workers = get_collection_url()
    
    print(f"Collection URL: {collection_url}")
    print(f"Save directory: {save_dir}")
    print(f"Max workers: {max_workers}")
    
    dataset_ids = get_datasets_from_collection(collection_url)
    print(f"Found {len(dataset_ids)} datasets.")
    results = parallel_download(dataset_ids, save_dir, max_workers)
    print("\nSummary:")
    for r in results:
        print(f"{r}\n")
