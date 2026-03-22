from flask import Flask, render_template, request, redirect, url_for, session
from utils.disease_lookup import clean_input
from api.uniprot_api import get_gene_from_disease, get_proteins
from api.chembl_api import get_drugs_from_gene
from visualization.graph import generate_graph_image
from utils.pdf_report import generate_pdf
import os
import traceback

app = Flask(__name__)
app.secret_key = "secret123"


@app.route("/", methods=["GET", "POST"])
def index():

    # 🔥 GET request
    if request.method == "GET":
        result = session.get("result")
        return render_template("index.html", result=result)

    # 🔥 POST request
    if request.method == "POST":
        try:
            disease = request.form["disease"]
            disease = clean_input(disease)

            symptoms = request.form.get("symptoms")

            gene = get_gene_from_disease(disease)

            if gene:
                proteins = get_proteins(gene)
                drugs = get_drugs_from_gene(gene, disease, symptoms)

                # 🔥 FDA fallback
                if not drugs:
                    from api.openfda_api import get_drugs_from_openfda
                    drugs = get_drugs_from_openfda(disease)

                # 🔥 Symptoms logic
                if symptoms:
                    print("User symptoms:", symptoms)
                    drugs.append({
                        "name": "Symptom-based Suggestion",
                        "score": 0.65,
                        "reasons": [f"Based on user symptoms: {symptoms}"]
                    })

                # 🔥 Message handling
                message = None

                if not drugs:
                    message = "No direct drug found. Research is ongoing for this disease."
                    drugs = [
                        {
                            "name": "Supportive Therapy",
                            "score": 0.6,
                            "reasons": ["General supportive care"]
                        }
                    ]

                # 🔥 GRAPH (safe)
                try:
                    generate_graph_image(disease, gene, proteins, drugs)
                    graph_path = "graph.png"
                except Exception as e:
                    print("Graph error:", e)
                    graph_path = None

                # 🔥 RESULT
                result = {
                    "disease": disease,
                    "gene": gene,
                    "proteins": proteins[:3] if proteins else [],
                    "drugs": drugs if drugs else [],
                    "message": message,
                    "pdf": "report.pdf",
                    "graph": graph_path
                }

                # 🔥 PDF (safe)
                try:
                    generate_pdf(result)
                except Exception as e:
                    print("PDF error:", e)

            else:
                result = {"error": "Disease not found"}

        except Exception as e:
            print("MAIN ERROR:\n", traceback.format_exc())
            result = {"error": "Something went wrong on server"}

        # 🔥 PRG pattern
        session["result"] = result
        return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)