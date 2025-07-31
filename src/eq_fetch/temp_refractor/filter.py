"""Module for filtering search and results."""

from typing import Any
import pandas as pd


def interactive_filter(results: Any) -> Any:
    """
    Interactively filter search results based on user input.
    Supports pandas DataFrame or list of dicts.
    Returns filtered results.
    """
    # Convert to DataFrame for easier filtering
    if isinstance(results, pd.DataFrame):
        df = results
    elif isinstance(results, list) and results and isinstance(results[0], dict):
        df = pd.DataFrame(results)
    else:
        print("Unsupported results type for filtering.")
        return results

    print(f"Current number of results: {len(df)}")
    while True:
        print("\nAvailable columns for filtering:", list(df.columns))
        col = input("Enter column to filter by (or press Enter to finish): ").strip()
        if not col or col not in df.columns:
            break
        op = input("Enter operator (==, !=, >, >=, <, <=, contains): ").strip()
        val = input("Enter value to compare: ").strip()

        # Try to cast value if column is numeric
        dtype = df[col].dtype
        try:
            if pd.api.types.is_numeric_dtype(dtype):
                val_cast = float(val)
            else:
                val_cast = val
        except Exception:
            val_cast = val

        if op == "==":
            df = df[df[col] == val_cast]
        elif op == "!=":
            df = df[df[col] != val_cast]
        elif op == ">":
            df = df[df[col] > val_cast]
        elif op == ">=":
            df = df[df[col] >= val_cast]
        elif op == "<":
            df = df[df[col] < val_cast]
        elif op == "<=":
            df = df[df[col] <= val_cast]
        elif op == "contains":
            df = df[df[col].astype(str).str.contains(str(val_cast), case=False)]
        else:
            print("Unknown operator. Try again.")
            continue

        print(f"Filtered number of results: {len(df)}")
        if len(df) == 0:
            print("No results left after filtering.")
            break

        cont = input("Filter further? (y/n): ").strip().lower()
        if cont != "y":
            break

    return df
