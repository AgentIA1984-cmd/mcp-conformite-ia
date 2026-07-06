#!/usr/bin/env python3
"""
conformite_ia_mcp — Serveur MCP de conformite IA (AI Act + RGPD, France/UE).

Fournit a un agent IA des outils pour :
- classer un systeme d'IA selon le niveau de risque de l'AI Act ;
- lister les obligations applicables par role et par niveau ;
- connaitre le calendrier d'application (echeances) ;
- rechercher une reference juridique (AI Act / RGPD) ;
- croiser un traitement de donnees avec les obligations RGPD.

Sources : Reglement (UE) 2024/1689 (AI Act), RGPD (2016/679), CNIL.
⚠️ Information et orientation reglementaire — ne constitue pas un conseil juridique.

Transport :
  MCP_TRANSPORT=stdio            (defaut, tests locaux)
  MCP_TRANSPORT=streamable-http  (production / MCP Hive) ; HOST, PORT en option.
"""

import json
import os
import unicodedata
from enum import Enum
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

import data

mcp = FastMCP(
    "conformite_ia_mcp",
    host=os.environ.get("HOST", "0.0.0.0"),
    port=int(os.environ.get("PORT", "8000")),
    # Mode recommande pour les serveurs distants / passerelles (MCP Hive) :
    # requetes independantes (pas de session a maintenir) + reponses JSON
    # (le client n'a pas besoin d'accepter text/event-stream).
    stateless_http=True,
    json_response=True,
)


# ==========================================================================
# Utilitaires partages
# ==========================================================================
def _normalize(text: str) -> str:
    """Minuscule + suppression des accents, pour une comparaison robuste."""
    text = (text or "").lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text


def _matches(text: str, keywords: List[str]) -> bool:
    return any(kw in text for kw in keywords)


def _detect_gpai(text: str) -> bool:
    return _matches(text, data.GPAI_KEYWORDS)


def _classify(description: str, domain: Optional[str] = None) -> Dict[str, Any]:
    """Logique de classification transparente et reproductible (mots-cles)."""
    text = _normalize(f"{description} {domain or ''}")

    for practice in data.PROHIBITED_PRACTICES:
        if _matches(text, practice["keywords"]):
            return {"tier": "prohibited", "hits": [practice], "gpai": _detect_gpai(text)}

    high_hits = [d for d in data.HIGH_RISK_DOMAINS if _matches(text, d["keywords"])]
    if high_hits:
        return {"tier": "high", "hits": high_hits, "gpai": _detect_gpai(text)}

    transp_hits = [t for t in data.TRANSPARENCY_OBLIGATIONS if _matches(text, t["keywords"])]
    if transp_hits:
        return {"tier": "limited", "hits": transp_hits, "gpai": _detect_gpai(text)}

    return {"tier": "minimal", "hits": [], "gpai": _detect_gpai(text)}


def _obligations_for(role: Optional[str], tier: str) -> Dict[str, List[str]]:
    roles = [role] if role in ("provider", "deployer") else ["provider", "deployer"]
    return {r: data.OBLIGATIONS.get((r, tier), []) for r in roles}


class ResponseFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"


class Role(str, Enum):
    PROVIDER = "provider"
    DEPLOYER = "deployer"


class RiskTier(str, Enum):
    PROHIBITED = "prohibited"
    HIGH = "high"
    LIMITED = "limited"
    MINIMAL = "minimal"


def _dump(payload: Dict[str, Any]) -> str:
    payload.setdefault("disclaimer", data.DISCLAIMER)
    payload.setdefault("sources", {"ai_act": data.AI_ACT_URL, "rgpd": data.GDPR_URL,
                                   "cnil": data.CNIL_URL})
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ==========================================================================
# Outil 1 — Classification d'un systeme d'IA
# ==========================================================================
class ClassifyInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    description: str = Field(..., min_length=3, max_length=2000,
                             description="Description du systeme d'IA et de son usage "
                                         "(ex. 'chatbot de tri des CV pour le recrutement').")
    domain: Optional[str] = Field(default=None, max_length=200,
                                  description="Domaine d'application optionnel "
                                              "(ex. 'ressources humaines', 'sante').")
    role: Optional[Role] = Field(default=None,
                                 description="Role de l'organisation : 'provider' "
                                             "(fournisseur) ou 'deployer' (deployeur).")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN,
                                            description="'markdown' ou 'json'.")

    @field_validator("description")
    @classmethod
    def _v(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("La description ne peut pas etre vide.")
        return v


@mcp.tool(
    name="classify_ai_system",
    annotations={"title": "Classer un systeme d'IA (AI Act)", "readOnlyHint": True,
                 "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def classify_ai_system(params: ClassifyInput) -> str:
    """Classe un systeme d'IA selon le niveau de risque du Reglement (UE) 2024/1689.

    Renvoie le niveau (prohibited / high / limited / minimal), la justification
    (pratiques ou domaines detectes avec l'article correspondant), les obligations
    applicables, l'echeance d'application et un rappel GPAI si un modele a usage
    general est detecte.

    Args:
        params (ClassifyInput): description, domaine optionnel, role optionnel, format.

    Returns:
        str: Markdown ou JSON. Schema JSON :
        {
          "risk_tier": str, "tier_label": str, "article": str,
          "applicable_since": str,
          "rationale": [{"id": str, "label": str, "article"/"annex": str}],
          "obligations": {"provider": [str], "deployer": [str]},
          "gpai_detected": bool, "gpai_note": str|null,
          "disclaimer": str, "sources": {...}
        }
    """
    result = _classify(params.description, params.domain)
    tier = result["tier"]
    meta = data.RISK_TIERS[tier]
    rationale = [{"id": h["id"], "label": h["label"],
                  "reference": h.get("article") or h.get("annex") or h.get("requirement", "")}
                 for h in result["hits"]]
    obligations = _obligations_for(params.role.value if params.role else None, tier)
    gpai_note = None
    if result["gpai"]:
        gpai_note = ("Modele a usage general (GPAI) detecte : obligations du Chapitre V "
                     "applicables depuis le 2 aout 2025 (Article 53).")

    payload = {
        "risk_tier": tier, "tier_label": meta["label"], "article": meta["article"],
        "applicable_since": meta["applicable_since"], "rationale": rationale,
        "obligations": obligations, "gpai_detected": result["gpai"], "gpai_note": gpai_note,
    }
    if params.response_format == ResponseFormat.JSON:
        return _dump(payload)

    lines = [f"# Classification AI Act — {meta['label']}", "",
             f"**Niveau :** `{tier}` ({meta['article']})",
             f"**Applicable depuis/le :** {meta['applicable_since']}",
             f"**Resume :** {meta['summary']}", ""]
    if rationale:
        lines.append("## Justification")
        for r in rationale:
            lines.append(f"- {r['label']} — *{r['reference']}*")
        lines.append("")
    else:
        lines += ["## Justification",
                  "- Aucune pratique interdite ni domaine a haut risque detecte.", ""]
    lines.append("## Obligations indicatives")
    for role, obs in obligations.items():
        role_fr = "Fournisseur" if role == "provider" else "Deployeur"
        lines.append(f"### {role_fr}")
        lines += [f"- {o}" for o in obs] or ["- —"]
        lines.append("")
    if gpai_note:
        lines += [f"> ⚠️ {gpai_note}", ""]
    lines += [f"_{data.DISCLAIMER}_", "",
              f"Sources : [AI Act]({data.AI_ACT_URL}) · [RGPD]({data.GDPR_URL}) · "
              f"[CNIL]({data.CNIL_URL})"]
    return "\n".join(lines)


# ==========================================================================
# Outil 2 — Obligations par role et niveau
# ==========================================================================
class ObligationsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    role: Role = Field(..., description="'provider' (fournisseur) ou 'deployer' (deployeur).")
    risk_tier: RiskTier = Field(..., description="Niveau : prohibited/high/limited/minimal.")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


@mcp.tool(
    name="list_obligations",
    annotations={"title": "Lister les obligations AI Act", "readOnlyHint": True,
                 "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def list_obligations(params: ObligationsInput) -> str:
    """Liste les obligations de l'AI Act pour un role et un niveau de risque donnes.

    Args:
        params (ObligationsInput): role, risk_tier, format.

    Returns:
        str: Markdown ou JSON {"role", "risk_tier", "obligations": [str], ...}.
    """
    obs = data.OBLIGATIONS.get((params.role.value, params.risk_tier.value), [])
    if params.response_format == ResponseFormat.JSON:
        return _dump({"role": params.role.value, "risk_tier": params.risk_tier.value,
                      "obligations": obs})
    role_fr = "Fournisseur" if params.role.value == "provider" else "Deployeur"
    lines = [f"# Obligations — {role_fr} / {data.RISK_TIERS[params.risk_tier.value]['label']}",
             ""]
    lines += [f"- {o}" for o in obs] or ["- —"]
    lines += ["", f"_{data.DISCLAIMER}_"]
    return "\n".join(lines)


# ==========================================================================
# Outil 3 — Calendrier d'application
# ==========================================================================
class DeadlinesInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    topic: Optional[str] = Field(default=None, max_length=100,
                                 description="Filtre optionnel (ex. 'gpai', 'haut risque', "
                                             "'transparence', 'interdit').")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


@mcp.tool(
    name="get_compliance_deadlines",
    annotations={"title": "Echeances d'application de l'AI Act", "readOnlyHint": True,
                 "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def get_compliance_deadlines(params: DeadlinesInput) -> str:
    """Renvoie le calendrier d'application de l'AI Act, filtrable par theme.

    Args:
        params (DeadlinesInput): topic optionnel, format.

    Returns:
        str: Markdown ou JSON {"deadlines": [{"date","milestone","scope"}], ...}.
    """
    items = data.TIMELINE
    if params.topic:
        t = _normalize(params.topic)
        items = [m for m in data.TIMELINE if t in _normalize(m["milestone"] + " " + m["scope"])]
        if not items:
            items = data.TIMELINE
    if params.response_format == ResponseFormat.JSON:
        return _dump({"deadlines": items})
    lines = ["# Calendrier d'application — AI Act", ""]
    for m in items:
        lines += [f"## {m['date']} — {m['milestone']}", m["scope"], ""]
    lines.append(f"_{data.DISCLAIMER}_")
    return "\n".join(lines)


# ==========================================================================
# Outil 4 — Recherche de reference juridique
# ==========================================================================
class LookupInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    query: str = Field(..., min_length=1, max_length=120,
                       description="Terme, numero d'article ou sujet "
                                   "(ex. 'article 5', 'transparence', 'DPO', 'article 22').")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


@mcp.tool(
    name="lookup_legal_reference",
    annotations={"title": "Rechercher une reference AI Act / RGPD", "readOnlyHint": True,
                 "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def lookup_legal_reference(params: LookupInput) -> str:
    """Recherche des articles de l'AI Act ou du RGPD par mot-cle ou numero.

    Args:
        params (LookupInput): query, format.

    Returns:
        str: Markdown ou JSON {"query", "results": [{"key","title","summary","url"}]}.
    """
    q = _normalize(params.query).replace("article", "art").replace("art.", "art").strip()
    q = q.replace("art ", "art_")
    results = []
    for key, ref in data.LEGAL_REFS.items():
        hay = _normalize(f"{key} {ref.get('title','')} {ref.get('summary','')}")
        if q in hay or q in _normalize(key):
            results.append({"key": key, "title": ref["title"],
                            "summary": ref.get("summary", ""), "url": ref["url"]})
    if params.response_format == ResponseFormat.JSON:
        return _dump({"query": params.query, "count": len(results), "results": results})
    if not results:
        return (f"Aucune reference trouvee pour '{params.query}'. "
                f"Essayez 'article 5', 'transparence', 'gpai', 'dpo', 'article 22'.")
    lines = [f"# References pour '{params.query}'", ""]
    for r in results:
        lines.append(f"## {r['title']}")
        if r["summary"]:
            lines.append(r["summary"])
        lines += [f"[Texte officiel]({r['url']})", ""]
    return "\n".join(lines)


# ==========================================================================
# Outil 5 — Croisement RGPD
# ==========================================================================
class GdprInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    description: str = Field(..., min_length=3, max_length=2000,
                             description="Description du traitement de donnees "
                                         "(ex. 'scoring de credit avec donnees de sante').")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


@mcp.tool(
    name="gdpr_crosscheck",
    annotations={"title": "Croiser un traitement avec le RGPD", "readOnlyHint": True,
                 "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def gdpr_crosscheck(params: GdprInput) -> str:
    """Identifie les obligations RGPD declenchees par un traitement de donnees.

    Args:
        params (GdprInput): description, format.

    Returns:
        str: Markdown ou JSON {"triggered": [{"label","obligations"}],
             "always": [str], "lawful_bases": [str], ...}.
    """
    text = _normalize(params.description)
    triggered = []
    for trig in data.GDPR_TRIGGERS:
        if _matches(text, trig["keywords"]):
            triggered.append({"id": trig["id"], "label": trig["label"],
                              "obligations": trig["obligations"]})
    if params.response_format == ResponseFormat.JSON:
        return _dump({"triggered": triggered, "always": data.GDPR_ALWAYS,
                      "lawful_bases": data.GDPR_LAWFUL_BASES})
    lines = ["# Croisement RGPD", ""]
    if triggered:
        lines.append("## Points d'attention detectes")
        for t in triggered:
            lines.append(f"### {t['label']}")
            lines += [f"- {o}" for o in t["obligations"]]
            lines.append("")
    else:
        lines += ["## Points d'attention detectes",
                  "- Aucun facteur de risque specifique detecte dans la description.", ""]
    lines.append("## Obligations dans tous les cas")
    lines += [f"- {o}" for o in data.GDPR_ALWAYS]
    lines += ["", "## Bases legales possibles (Article 6)"]
    lines += [f"- {b}" for b in data.GDPR_LAWFUL_BASES]
    lines += ["", f"_{data.DISCLAIMER}_",
              f"Source : [RGPD]({data.GDPR_URL}) · [CNIL]({data.CNIL_URL})"]
    return "\n".join(lines)


# ==========================================================================
# Point d'entree
# ==========================================================================
if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT", "stdio").lower().replace("_", "-")
    if transport in ("http", "streamable-http", "streamablehttp"):
        mcp.run(transport="streamable-http")
    elif transport == "sse":
        mcp.run(transport="sse")
    else:
        mcp.run()
