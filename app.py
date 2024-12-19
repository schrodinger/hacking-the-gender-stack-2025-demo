from flask import Flask, Response, redirect, render_template, request

from chemistry import search_compounds, smiles_to_svg, get_highlighted_image

app = Flask(__name__)


@app.route("/", methods=["GET"], endpoint="get_compounds")
def get_compounds():
    smiles_query = request.args.get("query", "")
    all_smiles = []
    with open("smiles.txt", "r") as file:
        content = file.read()
        all_smiles = content.split("\n")

    smiles_matching_query = all_smiles
    if smiles_query != "":
        match_indices_list = search_compounds(smiles_query, all_smiles)
        smiles_matching_query = [
            all_smiles[i]
            for i, match_indices in enumerate(match_indices_list)
            if len(match_indices) > 0
        ]

    return render_template(
        "compounds.html", smiles_list=smiles_matching_query, smiles_query=smiles_query
    )


@app.route("/compounds", methods=["POST"], endpoint="add_compounds")
def add_compounds():
    smiles = request.form.get("smiles_list")
    smiles_list = [s.strip() for s in smiles.splitlines() if s.strip() != ""]
    with open("smiles.txt", "a") as file:
        file.write("\n" + "\n".join(smiles_list))

    # Redirect back to the page you were on
    return redirect(request.headers.get("Referer"))


@app.route("/compound-image", methods=["GET"], endpoint="get_compound_image")
def get_compound_image():
    smiles = request.args.get("smiles", "")
    highlighted_substructure = request.args.get("highlight", "")
    if highlighted_substructure == "":
        return Response(smiles_to_svg(smiles), mimetype="image/svg+xml")
    else:
        return Response(
            get_highlighted_image(smiles, highlighted_substructure),
            mimetype="image/svg+xml",
        )
