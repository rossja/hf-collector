import os
import requests
from bs4 import BeautifulSoup
from subprocess import run

COLLECTION_URL = "https://huggingface.co/collections/common-pile/common-pile-v01-raw-data-6826b454a5a6a445d0b51b37"
CLONE_DIR = "hf_dataset_repos"

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
    ids = get_dataset_ids(COLLECTION_URL)
    print(f"Found {len(ids)} dataset repos.")
    git_clone_datasets(ids, CLONE_DIR)

