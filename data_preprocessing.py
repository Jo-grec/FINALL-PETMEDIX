import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Convert categorical variables to dummy variables
df_numeric = pd.get_dummies(df)

# Create a new DataFrame for scaled data with proper dtypes
dataset_scaled = pd.DataFrame(index=df_numeric.index, columns=df_numeric.columns, dtype=float)

# Scale the data
scaler = MinMaxScaler()
dataset_scaled[:] = scaler.fit_transform(df_numeric)

# Split features and target
X = dataset_scaled.drop("Exited", axis=1)
y = dataset_scaled["Exited"]

# Display the first few rows of the scaled dataset
print("Scaled Dataset Head:")
print(dataset_scaled.head()) 