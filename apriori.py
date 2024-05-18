from tkinter import simpledialog
import pandas as pd
from math import ceil
import itertools
from collections import Counter, defaultdict
import customtkinter


def load_transactions(file_path):
    df = pd.read_csv(file_path)
    percentage = simpledialog.askinteger(
        "Percentage",
        "Enter the percentage of records to load (e.g., 50 for 50%):",
    )
    num_records = int(len(df) * percentage / 100)
    selected_records = df.head(num_records)[["TransactionNo", "Items"]]
    # transactions_dict = (
    #     selected_records.groupby("TransactionNo")["Items"]
    #     .apply(lambda x: x.str.split(",").explode().tolist())
    #     .to_dict()
    # )
    transactions_dict = (
        selected_records.groupby("TransactionNo")["Items"]
        .apply(lambda x: list(set(x.str.split(",").explode())))
        .to_dict()
    )
    return transactions_dict


def generate_candidates(prev_candidates, k):
    """Generate candidate itemsets of size k."""
    candidates = set()
    for i in range(len(prev_candidates)):
        for j in range(i + 1, len(prev_candidates)):
            itemset1 = prev_candidates[i]
            itemset2 = prev_candidates[j]
            if itemset1[: k - 2] == itemset2[: k - 2]:
                candidates.add(tuple(sorted(set(itemset1) | set(itemset2))))
    return list(candidates)


def calculate_support(transactions, candidate_itemset):
    """Calculate the support count for a candidate itemset."""
    count = 0
    for transaction in transactions.values():
        if set(candidate_itemset).issubset(set(transaction)):
            count += 1
    return count


def apriori(transactions, min_support):
    """Apriori algorithm to find frequent itemsets."""
    # Step 1: Generate frequent 1-itemsets
    item_counts = defaultdict(int)
    for transaction in transactions.values():
        for item in transaction:
            item_counts[(item,)] += 1

    frequent_itemsets = {
        1: {
            itemset: support
            for itemset, support in item_counts.items()
            if support >= min_support
        }
    }
    k = 2

    # Steps 2 & 3: Generate frequent k-itemsets
    while frequent_itemsets[k - 1]:
        candidate_itemsets = generate_candidates(
            list(frequent_itemsets[k - 1].keys()), k
        )
        candidate_supports = {}
        for candidate in candidate_itemsets:
            support = calculate_support(transactions, candidate)
            if support >= min_support:
                candidate_supports[candidate] = support
        frequent_itemsets[k] = candidate_supports
        k += 1

    return frequent_itemsets


def generate_association_rules(frequent_itemsets, min_confidence):
    association_rules = []
    for itemset_length, itemsets in frequent_itemsets.items():
        if itemset_length < 2:  # Association rules require at least 2 items
            continue
        for itemset, support in itemsets.items():
            for i in range(1, len(itemset)):
                for antecedent in itertools.combinations(itemset, i):
                    antecedent = tuple(sorted(antecedent))
                    consequent = tuple(sorted(set(itemset) - set(antecedent)))
                    confidence = (
                        support / frequent_itemsets[len(antecedent)][antecedent]
                    )
                    if confidence >= min_confidence:
                        association_rules.append((antecedent, consequent, confidence))
    return association_rules


def print_frequent_itemsets(frequent_itemsets):
    for k, itemsets in frequent_itemsets.items():
        print(f"Frequent {k}-itemsets:")
        for itemset, support in itemsets.items():
            print(f"{', '.join(itemset)}   -> Support: {support}")
        print()


def print_association_rules(association_rules):
    for antecedent, consequent, confidence in association_rules:
        print(
            f"{', '.join(antecedent)} -> {', '.join(consequent)} : Confidence = {confidence:.2f}"
        )


if __name__ == "__main__":
    # Data = load_transactions("Bakery.csv", 100)

    Transactions = load_transactions("Bakery.csv", 100)
    min_support = 50
    min_confidence = 0.5
    # print(Transactions)

    frequent_itemsets = apriori(Transactions, min_support)
    print_frequent_itemsets(frequent_itemsets)

    association_rules = generate_association_rules(frequent_itemsets, min_confidence)

    # Print association rules with confidence
    print("Association Rules with Confidence:")
    print_association_rules(association_rules)
