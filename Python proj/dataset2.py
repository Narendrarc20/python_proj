import matplotlib.pyplot as plt

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Group by Date and sum cases
cases_over_time = df.groupby("Date")["Confirmed Cases"].sum()

# Plot
plt.figure(figsize=(10,5))
plt.plot(cases_over_time, marker="o", linestyle="-", color="blue")
plt.xlabel("Date")
plt.ylabel("Total Confirmed Cases")
plt.title("COVID-19 Cases Over Time")
plt.xticks(rotation=45)
plt.show()
