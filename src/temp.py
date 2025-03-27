
import pandas as pd

# File paths
csv_path = "./data/votes/Flagler/results.csv"  # Update with your actual file path

csv = pd.read_csv(csv_path)

for row in csv.iterrows():
    row[1]["Mail Votes"] = row[1]["Mail Votes"].replace(",", "")
    csv.at[row[0], "Mail Votes"] = row[1]["Mail Votes"]

csv.to_csv(csv_path, index=False)