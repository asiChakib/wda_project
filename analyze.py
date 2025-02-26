import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "primeapplehbomax.csv"
data = pd.read_csv(file_path)

# Calculate the number of backlinks per country for each company
backlinks_per_country = data.groupby("CountryCode")[["BackLinks_primevideo.com", "BackLinks_tv.apple.com", "BackLinks_max.com"]].sum()

# Identify major players (referring domains) clearly biased toward one company
def identify_major_players(row):
    # Check if one company has significantly more backlinks than the others
    max_value = max(row["BackLinks_primevideo.com"], row["BackLinks_tv.apple.com"], row["BackLinks_max.com"])
    if max_value > 2 * (row["BackLinks_primevideo.com"] + row["BackLinks_tv.apple.com"] + row["BackLinks_max.com"] - max_value):
        if max_value == row["BackLinks_primevideo.com"]:
            return "viaplay.com"
        elif max_value == row["BackLinks_tv.apple.com"]:
            return "youtube.com"
        elif max_value == row["BackLinks_max.com"]:
            return "voyo.nova.cz"
    return "Balanced"

data["MajorPlayer"] = data.apply(identify_major_players, axis=1)

# Save the results to a text file
output_file = "primeapplehbomax.txt"
with open(output_file, "w") as f:
    f.write("Backlinks per Country:\n")
    f.write(backlinks_per_country.to_string())
    f.write("\n\nMajor Players (Domains clearly biased):\n")
    for index, row in data.iterrows():
        if row["MajorPlayer"] != "Balanced":
            f.write(f"{row['Domain']} is biased towards {row['MajorPlayer']}\n")

# Visualize the analysis
backlinks_per_country.plot(kind="bar", figsize=(10, 6))
plt.title("Backlinks per Country for Each Company")
plt.xlabel("Country Code")
plt.ylabel("Number of Backlinks")
plt.legend(["viaplay.com", "youtube.com", "voyo.nova.cz"])
plt.tight_layout()
plt.savefig("primeapplehbomax.png")
plt.show()