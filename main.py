import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

n = 1000

regions = ["North", "South", "East", "West"]
age_groups = ["18-25", "26-35", "36-50"]
genders = ["Male", "Female"]

# Smart bias logic
def generate_choice(region):
    if region == "North":
        return np.random.choice(["Product A", "Product B", "Product C"], p=[0.6, 0.25, 0.15])
    elif region == "South":
        return np.random.choice(["Product A", "Product B", "Product C"], p=[0.4, 0.4, 0.2])
    elif region == "East":
        return np.random.choice(["Product A", "Product B", "Product C"], p=[0.5, 0.3, 0.2])
    else:
        return np.random.choice(["Product A", "Product B", "Product C"], p=[0.45, 0.3, 0.25])

data = []

for i in range(n):
    region = np.random.choice(regions)
    age = np.random.choice(age_groups)
    gender = np.random.choice(genders)
    choice = generate_choice(region)

    data.append([region, age, gender, choice])

df = pd.DataFrame(data, columns=["Region", "Age_Group", "Gender", "Choice"])

# Add date trend
df["Date"] = pd.date_range(start="2024-01-01", periods=n)

df.to_csv("data/poll_data.csv", index=False)

print("✅ Smart dataset created!")

# -----------------------
# ANALYSIS
# -----------------------
vote_counts = df["Choice"].value_counts()
print(vote_counts)

# -----------------------
# VISUALIZATION
# -----------------------
vote_counts.plot(kind='bar')
plt.savefig("images/bar_chart.png")
plt.close()