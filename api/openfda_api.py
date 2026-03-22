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
            name = item.get("openfda", {}).get("brand_name", ["Unknown"])[0]

            drugs.append({
                "name": name,
                "score": 0.85,
                "reasons": [
                    f"Approved drug for {disease}",
                    "Data sourced from FDA records"
                ]
            })

        return drugs

    except:
        return []