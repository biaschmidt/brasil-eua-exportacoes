"""
fetch_comex_br_us.py
Script example to fetch Brazil -> United States exports by HS2 (chapter) from ComexStat API
Save output as `export_br_us_by_chapter.csv`.
"""

import requests
import pandas as pd
import time

BASE = "https://api-comexstat.mdic.gov.br"

def get_country_values(language="pt"):
    """
    Query the list of available values for the 'country' filter.
    Returns a list of dicts with each value (label/code).
    """
    url = f"{BASE}/general/filters/country"
    params = {"language": language}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    payload = r.json()
    # payload structure: { "data": { "list": [ ... ] }, ... } (see docs)
    data = payload.get("data", {})
    # try multiple shapes defensively
    if isinstance(data, dict) and "list" in data:
        return data["list"]
    # fallback: return raw data
    return data

def find_country_value(country_list, query_terms=("United", "United States", "Estados Unidos", "USA", "United States of America")):
    """
    Try to find the entry for the United States in the list returned by the API.
    Returns the 'value' field (or the full entry) to be used in the query.
    """
    for item in country_list:
        # item might be dict with keys like 'value' and 'text' or similar
        text = str(item.get("text") or item.get("label") or item.get("value") or "").lower()
        for q in query_terms:
            if q.lower() in text:
                return item
    # fallback: try exact matches on common codes
    for item in country_list:
        val = str(item.get("value","")).lower()
        if val in ("usa","us","united states","united states of america"):
            return item
    return None

def query_exports_for_country(country_value, start_year=2000, end_year=2024, per_page=10000):
    """
    Send the main query to ComexStat to get export data grouped by chapter (HS2) and year.
    The exact body keys may vary with API version; this body follows fields used in ComexStat docs.
    """
    url = f"{BASE}/general"
    body = {
        # flow: "export" or "import"
        "flow": "export",
        # group by HS chapter (SH2) and year
        "groupBy": ["chapter", "year"],
        # metrics: fob is the standard value (check /general/metrics if needed)
        "metrics": ["fob"],
        # filters: country = destination country
        # Depending on the API, the filter object might be {"filter":"country","values":[<value>]}
        "filters": [
            {
                "filter": "country",
                # use 'value' or 'values' depending on what the filters endpoint returned;
                # we'll try both keys (the API usually accepts 'values' as list)
                "values": [country_value.get("value") if isinstance(country_value, dict) else country_value]
            }
        ],
        # timeframe: define the years range
        "startYear": start_year,
        "endYear": end_year,
        # pagination: large per_page to get all results (server may limit)
        "pagination": {"page": 1, "perPage": per_page},
        # language optional
        "language": "pt"
    }
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, json=body, headers=headers, timeout=60)
    r.raise_for_status()
    return r.json()

def normalize_response_to_df(resp_json):
    """
    Normalizes the API response into a pandas DataFrame.
    The structure of response varies, but usually contains 'data' with 'list' or rows.
    """
    # try common shapes
    if not isinstance(resp_json, dict):
        raise ValueError("Unexpected response format")
    data = resp_json.get("data")
    if data is None:
        # sometimes response may put rows directly at top-level
        rows = resp_json.get("rows") or resp_json.get("list") or []
    else:
        # check common nested keys
        if isinstance(data, dict):
            rows = data.get("rows") or data.get("list") or []
        else:
            rows = data
    # if rows is a dict mapping numeric keys -> items, convert to list
    if isinstance(rows, dict):
        rows = list(rows.values())
    # try to convert to dataframe
    df = pd.json_normalize(rows)
    return df

def main():
    print("1) Retrieving country filter values from ComexStat API...")
    try:
        country_list = get_country_values(language="pt")
    except Exception as e:
        print("Error fetching country list:", e)
        return

    print(f"Retrieved {len(country_list)} country entries (sample):", country_list[:3])

    country_item = find_country_value(country_list)
    if not country_item:
        print("Could not detect United States entry automatically. Inspect country_list and pick the correct 'value' manually.")
        # optional: print candidates
        for item in country_list:
            txt = item.get("text") or item.get("label") or item.get("value")
            if txt and ("estados" in str(txt).lower() or "united" in str(txt).lower() or "usa" in str(txt).lower()):
                print("Candidate:", item)
        return

    print("Detected country entry for USA:", country_item)
    # Use the 'value' field from the country_item in the main query
    country_value = country_item.get("value") if isinstance(country_item, dict) else country_item

    print("2) Querying export data (this may take a few seconds)...")
    try:
        resp = query_exports_for_country(country_item, start_year=2000, end_year=2024)
    except Exception as e:
        print("Error querying exports:", e)
        return

    print("3) Normalizing response into DataFrame...")
    try:
        df = normalize_response_to_df(resp)
    except Exception as e:
        print("Error normalizing response:", e)
        print("Full response preview:", resp)
        return

    if df.empty:
        print("No rows returned. Inspect the raw response:")
        print(resp)
        return

    # Save CSV
    out_csv = "export_br_us_by_chapter.csv"
    df.to_csv(out_csv, index=False)
    print(f"Saved results to {out_csv}. Preview:")
    print(df.head(10))

if __name__ == "__main__":
    main()
