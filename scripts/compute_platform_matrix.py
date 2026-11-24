"""Recalcular la matriz ponderada de plataformas y su análisis de sensibilidad.

Uso: ``python scripts/compute_platform_matrix.py`` (imprime tablas Markdown
que se copian en ``docs/matriz_plataformas.md``).
"""

PLATFORMS = ("Dialogflow CX", "Copilot Studio", "Botpress Cloud",
             "RAG Python + Ollama")

# Puntaje 1–5 por criterio y plataforma (mismo orden que PLATFORMS).
SCORES = {
    "costo": (2, 3, 4, 5),
    "rag_citas": (4, 4, 3, 5),
    "low_code": (4, 5, 4, 1),
    "publicacion": (3, 3, 4, 3),
    "espanol": (4, 4, 4, 4),
    "analitica": (4, 5, 3, 2),
    "control": (2, 2, 2, 5),
}
CRITERIA_LABELS = {
    "costo": "Costo para el autor",
    "rag_citas": "RAG gestionado sobre documentos con citas",
    "low_code": "Desarrollo low-code y protocolo visual",
    "publicacion": "Publicación web pública",
    "espanol": "Calidad en español",
    "analitica": "Analítica y evaluación integradas",
    "control": "Control y reproducibilidad",
}
SCENARIOS = {
    "A. Low-code (elegido)": {
        "costo": 25, "rag_citas": 20, "low_code": 20, "publicacion": 15,
        "espanol": 10, "analitica": 10, "control": 0,
    },
    "B. Costo y control": {
        "costo": 30, "rag_citas": 20, "low_code": 5, "publicacion": 15,
        "espanol": 10, "analitica": 5, "control": 15,
    },
    "C. Igual que A, Copilot Studio con pago por uso (costo = 2)": {
        "costo": 25, "rag_citas": 20, "low_code": 20, "publicacion": 15,
        "espanol": 10, "analitica": 10, "control": 0,
    },
}
SCENARIO_OVERRIDES = {
    "C. Igual que A, Copilot Studio con pago por uso (costo = 2)": {
        ("costo", "Copilot Studio"): 2,
    },
}


def score(criterion: str, platform: str, scenario: str) -> int:
    """Obtener el puntaje de una plataforma en un criterio y escenario.

    :param criterion: clave del criterio.
    :param platform: nombre de la plataforma.
    :param scenario: nombre del escenario.
    :return: puntaje 1–5.
    """
    override = SCENARIO_OVERRIDES.get(scenario, {})
    if (criterion, platform) in override:
        return override[(criterion, platform)]
    return SCORES[criterion][PLATFORMS.index(platform)]


def weighted_scores(scenario: str) -> dict[str, float]:
    """Calcular el puntaje ponderado de cada plataforma en un escenario.

    :param scenario: nombre del escenario.
    :return: puntaje ponderado por plataforma.
    :raises ValueError: si los pesos no suman 100.
    """
    weights = SCENARIOS[scenario]
    if sum(weights.values()) != 100:
        raise ValueError(f"Los pesos de '{scenario}' no suman 100")
    return {
        platform: sum(
            weight * score(criterion, platform, scenario)
            for criterion, weight in weights.items()
        ) / 100
        for platform in PLATFORMS
    }


def format_number(value: float) -> str:
    """Formatear con coma decimal y dos decimales.

    :param value: número.
    :return: texto como ``3,90``.
    """
    return f"{value:.2f}".replace(".", ",")


def render_matrix(scenario: str) -> str:
    """Generar la tabla Markdown de un escenario.

    :param scenario: nombre del escenario.
    :return: tabla Markdown.
    """
    weights = SCENARIOS[scenario]
    totals = weighted_scores(scenario)
    best = max(totals, key=totals.get)
    rows = [
        "| Criterio (peso) | " + " | ".join(PLATFORMS) + " |",
        "|---|" + "---|" * len(PLATFORMS),
    ]
    for criterion, weight in weights.items():
        if not weight:
            continue
        cells = " | ".join(
            str(score(criterion, platform, scenario)) for platform in PLATFORMS
        )
        rows.append(f"| {CRITERIA_LABELS[criterion]} ({weight} %) | {cells} |")
    cells = " | ".join(
        f"**{format_number(totals[p])}**" if p == best
        else format_number(totals[p])
        for p in PLATFORMS
    )
    rows.append(f"| **Puntaje ponderado** | {cells} |")
    return "\n".join(rows)


def main() -> None:
    """Imprimir las tablas de todos los escenarios."""
    for scenario in SCENARIOS:
        print(f"### {scenario}\n\n{render_matrix(scenario)}\n")


if __name__ == "__main__":
    main()
