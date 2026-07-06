# conformite_ia_mcp — Conformité IA (AI Act + RGPD)

Serveur MCP qui donne à un agent IA des outils de conformité réglementaire pour le marché français/européen, à partir des textes officiels (Règlement UE 2024/1689, RGPD, CNIL).

> ⚠️ **Information et orientation réglementaire — ne constitue pas un conseil juridique.**

## Outils

| Outil | Rôle |
|-------|------|
| `classify_ai_system` | Classe un système d'IA (interdit / haut risque / limité / minimal) + obligations + échéance |
| `list_obligations` | Obligations par rôle (fournisseur/déployeur) et niveau de risque |
| `get_compliance_deadlines` | Calendrier d'application de l'AI Act (filtrable) |
| `lookup_legal_reference` | Recherche d'articles AI Act / RGPD avec liens officiels |
| `gdpr_crosscheck` | Obligations RGPD déclenchées par un traitement de données |

## Lancer en local (STDIO)

```bash
pip install -r requirements.txt
python test_local.py          # tests hors ligne
python server.py              # STDIO (défaut)
```

Inspecter avec l'inspecteur MCP :

```bash
npx @modelcontextprotocol/inspector python server.py
```

## Lancer en HTTP (production / MCP Hive)

```bash
MCP_TRANSPORT=streamable-http HOST=0.0.0.0 PORT=8000 python server.py
# Endpoint : http://<hôte>:8000/mcp   (Streamable HTTP)
```

Ou via Docker :

```bash
docker build -t conformite-ia-mcp .
docker run -p 8000:8000 conformite-ia-mcp
```

## Dépôt sur MCP Hive

Voir `HIVE_LISTING.md` (nom, catégorie, description, liste d'outils, pricing suggéré). Hive attend un serveur **Streamable HTTP + en-tête clé API**.

## Sources

- [AI Act — Règlement (UE) 2024/1689](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32024R1689)
- [RGPD — Règlement (UE) 2016/679](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32016R0679)
- [CNIL](https://www.cnil.fr)
