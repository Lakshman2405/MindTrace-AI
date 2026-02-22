import os
import pandas as pd
from datasets import load_dataset

print("Downloading GoEmotions dataset...")

# Load dataset (from cache if already downloaded)
dataset = load_dataset("go_emotions", "simplified")

# Create local project storage path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "go_emotions")

os.makedirs(DATA_DIR, exist_ok=True)

print("Saving dataset as CSV files...")

# Save each split as CSV
pd.DataFrame(dataset["train"]).to_csv(
    os.path.join(DATA_DIR, "train.csv"),
    index=False
)

pd.DataFrame(dataset["validation"]).to_csv(
    os.path.join(DATA_DIR, "validation.csv"),
    index=False
)

pd.DataFrame(dataset["test"]).to_csv(
    os.path.join(DATA_DIR, "test.csv"),
    index=False
)

print("GoEmotions dataset stored inside /data/go_emotions/")
print("Download and storage complete!")
