# eda.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/food_nutrition.csv")
print("Dataset head:\n", df.head())
print("\nStats:\n", df.describe())

# Histogram of calories
plt.figure(figsize=(6,4))
sns.histplot(df['calories'], kde=True)
plt.title("Calories distribution (sample Indian dishes)")
plt.savefig("calories_histogram.png")
plt.close()

# Pie: veg vs non-veg
plt.figure(figsize=(5,5))
counts = df['veg'].value_counts()
plt.pie(counts, labels=counts.index, autopct='%1.1f%%')
plt.title("Veg vs Non-Veg distribution")
plt.savefig("veg_pie.png")
plt.close()

print("EDA plots saved: calories_histogram.png, veg_pie.png")
