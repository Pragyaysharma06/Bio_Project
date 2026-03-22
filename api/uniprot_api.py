import requests


# 🔥 Duplicate remover (order safe)
def remove_duplicates(items):
    seen = set()
    result = []

    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result


def get_gene_from_disease(disease):
    url = f"https://rest.uniprot.org/uniprotkb/search?query={disease}&format=json"
    
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    try:
        for entry in data["results"]:
            gene = entry["genes"][0]["geneName"]["value"]
            return gene
    except:
        return None


def get_proteins(gene):
    url = f"https://rest.uniprot.org/uniprotkb/search?query={gene}&format=json"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    proteins = []

    try:
        for entry in data["results"]:
            protein = entry["proteinDescription"]["recommendedName"]["fullName"]["value"]
            proteins.append(protein)
    except:
        pass

    # 🔥 APPLY DUPLICATE REMOVAL
    proteins = remove_duplicates(proteins)

    return proteins