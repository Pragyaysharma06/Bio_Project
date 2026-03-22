import requests

def get_drugs_from_openfda(disease):
    try:
        url = f"https://api.fda.gov/drug/label.json?search=indications_and_usage:{disease}&limit=3"
        response = requests.get(url)

        if response.status_code != 200:
            return []

        data = response.json()

        drugs = []

        for item in data.get("results", []):
            name = item.get("openfda", {}).get("brand_name")

            if name:
                name = name[0]
            else:
                name = item.get("openfda", {}).get("generic_name", ["Unknown"])[0]

# ❌ skip unknown completely
            if name == "Unknown":
                continue

            drugs.append({
                "name": name,
                "score": 0.85,
                "reasons": [
                    f"Commonly prescribed for managing {disease}",
                    "Acts on biological pathways related to the condition",
                    "Clinically used in standard treatment protocols"
                ]
            })

        return drugs

    except:
        return []