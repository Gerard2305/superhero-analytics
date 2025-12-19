from difflib import get_close_matches


def search_hero(query: str, heroes, limit=5):
    names = {hero.name.lower(): hero for hero in heroes}

    query = query.lower().strip()

    # Match exacto
    if query in names:
        return [names[query]]

    # Match parcial
    partials = [
        hero for hero in heroes
        if query in hero.name.lower()
    ]

    if partials:
        return partials[:limit]

    # Sugerencias
    suggestions = get_close_matches(
        query,
        names.keys(),
        n=limit,
        cutoff=0.6
    )

    return [names[name] for name in suggestions]
