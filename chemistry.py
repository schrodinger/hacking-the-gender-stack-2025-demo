from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.DataStructs.cDataStructs import ExplicitBitVect

from typing import List

SUBSTRUCTURE_FP_SIZE = 2048

EXAMPLE_COMPOUNDS = [
    # smiles, substructure fingerprint
    "CCC(Cl)C(N)C1=CC=CC=C1",
    "CCC(Cl)C(F)C1=CC=CC=C1",
    "CCC(Cl)C(F)C1CCCCC1",
    "CCC(Cl)C(N)C1CCCCC1",
    "CCC(F)C(Cl)CC",
    "CCC(F)C(N)CC",
    "CCC(Cl)C(N)C1CCC2CCCCC2C1",
]


def smiles_to_svg(smiles: str, width: int = 400, height: int = 400) -> bytes:
    """
    makes an SVG image of a molecule
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise RuntimeError("Invalid SMILES")

    Chem.rdCoordGen.AddCoords(mol)
    drawer = Chem.Draw.rdMolDraw2D.MolDraw2DSVG(width, height)
    # set drawing options on drawer.getOptions()
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    return drawer.GetDrawingText().encode()


def get_substructure_fingerprint(mol):
    """
    TODO: substructure fingerprints
    returns substructure fingerprint for mol
    """
    fp = ExplicitBitVect(SUBSTRUCTURE_FP_SIZE, True)
    return fp  # this is currently empty and useless


def get_highlighted_image(
    target_smiles: str, query_smiles: str, width: int = 400, height: int = 400
):
    """
    TODO: Creates image of highlighted molecule
    """
    target_mol = Chem.MolFromSmiles(target_smiles)
    query_mol = Chem.MolFromSmiles(query_smiles)
    match = target_mol.GetSubstructMatch(query_mol)

    Chem.rdCoordGen.AddCoords(target_mol)
    Chem.rdCoordGen.AddCoords(query_mol)

    drawer = Chem.Draw.rdMolDraw2D.MolDraw2DSVG(width, height)
    drawer.DrawMolecule(target_mol, highlightAtoms=match)
    drawer.FinishDrawing()
    return drawer.GetDrawingText().encode()


def search_compounds(
    query_smiles: str, compound_list: List[str] = EXAMPLE_COMPOUNDS
) -> List[List[int]]:
    """
    search the list of smiles and return substructure match indices

    is empty list if not match and that index

    it would be nice to fingerprint and store fingerprints in memory
    """
    query_mol = Chem.MolFromSmiles(query_smiles)
    if query_mol is None:
        raise RuntimeError("Invalid query SMILES")

    compounds = [Chem.MolFromSmiles(s) for s in compound_list]
    matches = []
    for m in compounds:
        if m is None:
            matches.append([])
        else:
            matches.append(m.GetSubstructMatch(query_mol))
    return matches


# print(search_compounds("C"))
# print(search_compounds("C1CCCCC1"))

# import rdkit
# print(rdkit.__version__)

# print(smiles_to_svg("CC"))
