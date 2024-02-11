"""

"""
import csv
import json


def write_to_csv(catalog, search, filename):
    """
    :param : 
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # Save search parameters
    # TODO: Remove empty params
    search_filename = str(filename)[:-4] + "_search.csv"
    print("Saving search parameters to ", search_filename)
    with open(search_filename, "w") as fout:
        writer = csv.DictWriter(fout, fieldnames=search.keys())
        writer.writeheader()
        writer.writerow(search)
    # Save catalog
    # TODO: expand articles list
    print("Saving catalog to ", filename)
    catalog.to_csv(filename)


def write_to_json(catalog, search, filename):
    """
    :param : 
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # Save search parameters
    # TODO: Remove empty params
    search_filename = str(filename)[:-5] + "_search.json"
    print("Saving search parameters to ", search_filename)

    with open(search_filename, "w") as fout:
        json.dump(search, fout, indent=2)

    # Save catalog
    # TODO: clean format
    print("Saving catalog to ", filename)
    catalog.to_json(filename)
