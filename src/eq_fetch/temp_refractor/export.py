"""Module for exports."""

from typing import Any
import pandas as pd
import dicttoxml


def export_results(results: Any, fmt: str, filename: str) -> None:
    """."""
    # Convert to DataFrame if needed
    if isinstance(results, pd.DataFrame):
        df = results
    elif isinstance(results, list) and results and isinstance(results[0], dict):
        df = pd.DataFrame(results)
    else:
        raise ValueError("Unsupported results type for export.")

    if fmt == "csv":
        df.to_csv(filename, index=False)
    elif fmt == "json":
        df.to_json(filename, orient="records", lines=True)
    elif fmt == "xml":
        try:
            df.to_xml(filename, index=False)
        except AttributeError:
            # For older pandas versions without to_xml

            xml_bytes = dicttoxml.dicttoxml(df.to_dict(orient="records"))
            with open(filename, "wb") as f:
                f.write(xml_bytes)
    else:
        raise ValueError(f"Unsupported export format: {fmt}")
