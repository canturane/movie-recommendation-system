import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Load user-movie matrix from CSV file
df = pd.read_csv("prepared_data/UserMovieMatrix.csv")

# Extract column 'userId'
df = df.drop(columns=["userId"])

# Preparing the matrix for the Apriori algorithm
min_support = 0.16
frequent_itemsets = apriori(
    df.astype(bool),
    min_support=min_support,
    use_colnames=True,
    max_len=2,
    low_memory=True,
)

# Association rules are being created
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.5)
rules.head()

# Print results to screen
print("Frequently Used")
print(frequent_itemsets)

print("\nAssociation Rules:")
print(rules)
# Save results
frequent_itemsets.to_csv("prepared_data/frequent.csv", index=False)
rules.to_csv("prepared_data/rules.csv", index=False)
