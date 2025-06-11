import os
import requests
from bs4 import BeautifulSoup
from datasets import load_dataset
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

COLLECTION_URL = "https://huggingface.co/collections/common-pile/common-pile-v01-raw-data-6826b454a5a6a445d0b51b37"
#COLLECTION_URL = "https://huggingface.co/collections/common-pile/common-pile-v01-raw-data-6826b454a5a6a445d0b51b37"
SAVE_DIR = "downloaded_datasets"
MAX_WORKERS = 4  # Adjust based on your bandwidth & CPU
USE_AUTH_TOKEN = False # set to True if you need auth to access the dataset

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

def download_and_save_dataset(dataset_id):
    """Download and save a single dataset locally."""
    local_path = os.path.join(SAVE_DIR, dataset_id.replace("/", "__"))
    if os.path.exists(local_path):
        return f"[SKIP] {dataset_id} already downloaded."

    try:
        dataset = load_dataset(dataset_id, use_auth_token=USE_AUTH_TOKEN)
        dataset.save_to_disk(local_path)
        return f"[OK] {dataset_id} saved to {local_path}"
    except Exception as e:
        return f"[FAIL] {dataset_id}: {e}"

def parallel_download(dataset_ids):
    os.makedirs(SAVE_DIR, exist_ok=True)
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(download_and_save_dataset, ds): ds for ds in dataset_ids}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading"):
            result = future.result()
            results.append(result)
    return results

if __name__ == "__main__":
    dataset_ids = get_datasets_from_collection(COLLECTION_URL)
    print(f"Found {len(dataset_ids)} datasets.")
    results = parallel_download(dataset_ids)
    print("\nSummary:")
    for r in results:
        print(f"{r}\n")
