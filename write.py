"""

"""
import csv
import json


def write_to_csv(catalog, search, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
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
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
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
