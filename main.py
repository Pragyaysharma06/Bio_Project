from utils.disease_lookup import clean_input
from api.uniprot_api import get_gene_from_disease, get_proteins
from visualization.graph import visualize_graph
from api.chembl_api import get_drugs_from_gene


def main():
    disease = input("Enter any disease: ")
    disease = clean_input(disease)

    print("\n🔍 Searching...")

    # Get gene dynamically
    gene = get_gene_from_disease(disease)

    if not gene:
        print("❌ Could not find gene for this disease")
        return

    print(f"\n🧬 Gene found: {gene}")

    # Get proteins
    proteins = get_proteins(gene)

    if not proteins:
        print("❌ No proteins found")
        return

    print("\n🧪 Proteins:")
    for p in proteins[:3]:
        print("-", p)

    # 🔥 GET DRUGS (INSIDE MAIN)
    print("\n💊 Fetching real drug data...")

    drugs = get_drugs_from_gene(gene)

    if drugs:
        print("\n💡 Drug Candidates:")
        for d in drugs[:5]:
            print("-", d)
    else:
        print("⚠ No drugs found")

    # 🔥 GRAPH (INSIDE MAIN)
    visualize_graph(disease, gene, proteins, drugs)


if __name__ == "__main__":
    main()