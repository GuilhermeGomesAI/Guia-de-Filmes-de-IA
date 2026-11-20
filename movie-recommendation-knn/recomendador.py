"""Sistema de recomendação de filmes com KNN (K-Nearest Neighbors).

Ideia: cada filme é um vetor de características (animação, aventura, comédia,
drama). O perfil do espectador é a média dos vetores dos filmes favoritos, e os
filmes recomendados são os vizinhos mais próximos desse perfil.
"""

import numpy as np
from sklearn.neighbors import NearestNeighbors

# 1. Catálogo pequeno de filmes -------------------------------------------------
# Cada coluna é uma característica: [animação, aventura, comédia, drama].
# Os valores são exemplos didáticos feitos à mão, não metadados oficiais.
CARACTERISTICAS = ["animação", "aventura", "comédia", "drama"]

FILMES = [
    "Toy Story",
    "Finding Nemo",
    "Monsters, Inc.",
    "The Incredibles",
    "Shrek",
    "Jurassic Park",
    "Indiana Jones",
    "The Hangover",
    "The Shawshank Redemption",
    "The Pursuit of Happyness",
]

CARACTERISTICAS_FILMES = np.array(
    [
        [1, 1, 1, 0],  # Toy Story
        [1, 1, 1, 0],  # Finding Nemo
        [1, 0, 1, 0],  # Monsters, Inc.
        [1, 1, 0, 0],  # The Incredibles
        [1, 0, 1, 0],  # Shrek
        [0, 1, 0, 0],  # Jurassic Park
        [0, 1, 1, 0],  # Indiana Jones
        [0, 0, 1, 0],  # The Hangover
        [0, 0, 0, 1],  # The Shawshank Redemption
        [0, 0, 0, 1],  # The Pursuit of Happyness
    ],
    dtype=float,
)


def criar_modelo(caracteristicas=CARACTERISTICAS_FILMES):
    """Ajusta o KNN ao catálogo inteiro, inclusive aos filmes ainda não vistos."""
    modelo = NearestNeighbors(metric="euclidean")
    modelo.fit(caracteristicas)
    return modelo


def ranking_de_filmes(favoritos, modelo=None, filmes=FILMES,
                      caracteristicas=CARACTERISTICAS_FILMES):
    """Devolve [(filme, distância), ...] dos mais próximos ao mais distante.

    Os filmes favoritos ficam de fora. Empates são resolvidos pela posição no
    catálogo, para que execuções repetidas gerem sempre a mesma ordem.
    """
    if modelo is None:
        modelo = criar_modelo(caracteristicas)

    desconhecidos = [f for f in favoritos if f not in filmes]
    if desconhecidos:
        raise ValueError(f"Filmes fora do catálogo: {', '.join(desconhecidos)}")

    posicoes_favoritos = [filmes.index(f) for f in favoritos]
    perfil = caracteristicas[posicoes_favoritos].mean(axis=0).reshape(1, -1)

    distancias, posicoes = modelo.kneighbors(perfil, n_neighbors=len(filmes))

    # Arredondar evita que ruído de ponto flutuante quebre o critério de desempate.
    ordenados = sorted(
        zip(np.round(distancias[0], 6), posicoes[0]),
        key=lambda par: (par[0], par[1]),
    )
    return [
        (filmes[posicao], float(distancia))
        for distancia, posicao in ordenados
        if filmes[posicao] not in favoritos
    ]


def recomendar_filmes(favoritos, quantidade=3, modelo=None):
    """Média dos favoritos conhecidos -> vizinhos próximos -> exclui os favoritos."""
    ranking = ranking_de_filmes(favoritos, modelo=modelo)
    return [filme for filme, _ in ranking[:quantidade]]


def main():
    # 2. Separa um favorito conhecido ANTES de recomendar.
    filmes_curtidos = ["Toy Story", "Monsters, Inc.", "Finding Nemo"]
    favorito_escondido = "Finding Nemo"
    outros_favoritos = [f for f in filmes_curtidos if f != favorito_escondido]

    # 3. O favorito escondido continua no catálogo, mas fora do histórico do espectador.
    modelo = criar_modelo()

    # 4. Gera as recomendações usando APENAS os favoritos restantes.
    recomendacoes = recomendar_filmes(outros_favoritos, quantidade=3, modelo=modelo)
    print("Favoritos usados:", ", ".join(outros_favoritos))
    print("\nFilmes recomendados:")
    for posicao, titulo in enumerate(recomendacoes, start=1):
        print(f"{posicao}. {titulo}")

    # 5. Teste: o favorito que escondemos apareceu entre as recomendações?
    passou = favorito_escondido in recomendacoes
    print("\nFavorito escondido:", favorito_escondido)
    print("Ele apareceu no nosso top 3?", passou)
    print("\nEste é apenas um teste pequeno com características feitas à mão, "
          "não é prova de qualidade no mundo real.")


if __name__ == "__main__":
    main()
