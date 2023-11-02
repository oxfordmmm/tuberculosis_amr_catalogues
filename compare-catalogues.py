"""Compare two catalogues to determine the differences.
Compares both the literal lines, as well as mutations
"""
import sys
import pandas as pd


def parse_cat(path: str) -> set:
    """Parse a file at a given path, returning a set of lines.

    Args:
        path (str): Path to a catalogue

    Returns:
        set: Set of lines in the file
    """
    with open(path) as f:
        return set([line.strip() for line in f])


def parse_cat_mutations(path: str) -> set:
    """Parse a catalogue at a given path, returning a set of (drug, mutation, prediction)
    from the catalogue.

    Args:
        path (str): Path to catalogue

    Returns:
        set: Set of (drug, mutation, prediction) from the catalogue
    """
    cat = pd.read_csv(path)
    mutations = set()
    for _, row in cat.iterrows():
        mutations.add((row["DRUG"], row["MUTATION"], row["PREDICTION"]))
    return mutations


if __name__ == "__main__":
    if len(sys.argv) not in [3, 4]:
        print("Usage: python compare-catalogues.py <path to cat1> <path to cat2> [-v]")
        sys.exit(0)

    if len(sys.argv) == 4:
        if sys.argv[3] != "-v":
            print(
                "Usage: python compare-catalogues.py <path to cat1> <path to cat2> [-v]"
            )
            sys.exit(0)
        verbose = True
    else:
        verbose = False

    cat1_path = sys.argv[1]
    cat2_path = sys.argv[2]

    cat1 = parse_cat(cat1_path)
    cat2 = parse_cat(cat2_path)

    cat1_mutations = parse_cat_mutations(cat1_path)
    cat2_mutations = parse_cat_mutations(cat2_path)

    print("LINE LITERAL COMPARISON")
    print("***********************")
    print("Catalogue 1 has length: ", len(cat1))
    print("Catalogue 2 has length: ", len(cat2))
    print()
    print("Common items between catalogues: ", len(cat1.intersection(cat2)))
    print("Items in catalogue 1 but not catalogue 2: ", len(cat1.difference(cat2)))
    print("Items in catalogue 2 but not catalogue 1: ", len(cat2.difference(cat1)))
    print()
    print("@@@@@@@@@@@@@@@@@@@@@@@")
    print()
    print("MUTATION COMPARISON")
    print("***********************")
    print(f"Catalogue 1 has {len(cat1_mutations)} unique mutations")
    print(f"Catalogue 2 has {len(cat2_mutations)} unique mutations")
    print()
    print(
        "Common items between catalogues: ",
        len(cat1_mutations.intersection(cat2_mutations)),
    )
    print(
        "Items in catalogue 1 but not catalogue 2: ",
        len(cat1_mutations.difference(cat2_mutations)),
    )
    if verbose:
        for drug, mutation, prediction in cat1_mutations.difference(cat2_mutations):
            print(drug, mutation, prediction)
        print()
    print(
        "Items in catalogue 2 but not catalogue 1: ",
        len(cat2_mutations.difference(cat1_mutations)),
    )
    if verbose:
        for drug, mutation, prediction in cat2_mutations.difference(cat1_mutations):
            print(drug, mutation, prediction)
        print()
