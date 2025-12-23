import pandas as pd

# Load your CSV
df = pd.read_csv("tiktok_dataset.csv")

# Filter only misinformation (assuming "False" marks wrong info)
misinfo_df = df[df["verified_status"] == "not verified"]

# Keep only the needed columns
result = misinfo_df[["video_transcription_text"]]

# Save to new CSV
result.to_csv("tt.txt", index=False)

print("Filtered dataset saved")

