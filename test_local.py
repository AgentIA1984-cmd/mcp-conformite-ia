#!/usr/bin/env python3
"""Test local du serveur conformite_ia_mcp (sans reseau)."""
import asyncio
import inspect
import server

CASES = [
    ("notation sociale des citoyens par une autorite publique", None, "prohibited"),
    ("reconnaissance des emotions des employes au travail", None, "prohibited"),
    ("chatbot de tri des CV pour le recrutement", "ressources humaines", "high"),
    ("scoring de credit pour l'octroi de prets bancaires", None, "high"),
    ("systeme d'admission et de notation des eleves", "education", "high"),
    ("assistant conversationnel qui repond aux clients", None, "limited"),
    ("generateur d'images de synthese pour le marketing", None, "limited"),
    ("outil interne d'optimisation de la logistique d'entrepot", None, "minimal"),
]


def main() -> None:
    tools = asyncio.run(server.mcp.list_tools())
    names = [t.name for t in tools]
    print("Outils enregistres :", names)
    assert len(tools) == 5, f"attendu 5 outils, obtenu {len(tools)}"

    ok = 0
    for desc, dom, expected in CASES:
        got = server._classify(desc, dom)["tier"]
        flag = "OK " if got == expected else "FAIL"
        ok += got == expected
        print(f"[{flag}] {desc[:48]:48s} -> {got:10s} (attendu {expected})")

    # GPAI detection
    assert server._detect_gpai(server._normalize("un grand modele de langage")) is True

    # Appel end-to-end d'un outil
    fn = server.classify_ai_system
    if inspect.iscoroutinefunction(fn):
        out = asyncio.run(fn(server.ClassifyInput(
            description="chatbot de tri des CV", role="provider",
            response_format="json")))
        assert '"risk_tier": "high"' in out
        print("\n--- classify_ai_system (json, extrait) ---")
        print(out[:500])

    print(f"\nClassification : {ok}/{len(CASES)} correctes | outils : {len(tools)}")
    assert ok == len(CASES), "Certaines classifications sont incorrectes."
    print("TOUS LES TESTS PASSENT.")


if __name__ == "__main__":
    main()
