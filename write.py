"""

"""
import csv
import json


def write_to_csv(catalog, filename):
    """
    :param :
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # Save search parameters
    search_filename = str(filename)[:-4] + "_search.csv"
    print("\n\nSaving search parameters to ", search_filename)
    search_params = catalog.get_params()
    with open(search_filename, "w") as fout:
        writer = csv.DictWriter(fout, fieldnames=search_params.keys())
        writer.writeheader()
        writer.writerow(search_params)
    # Save catalog
    print("\nSaving catalog to ", filename)
    results = catalog.earthquake_catalog
    results.to_csv(filename)


def write_to_json(catalog, filename):
    """
    :param :
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # Save search parameters
    search_filename = str(filename)[:-5] + "_search.json"
    print("\n\nSaving search parameters to ", search_filename)

    search_params = catalog.get_params()
    with open(search_filename, "w") as fout:
        json.dump(search_params, fout, indent=2)

    # Save catalog
    # TODO: clean format
    print("\nSaving catalog to ", filename)
    results = catalog.earthquake_catalog
    results.to_json(filename)
