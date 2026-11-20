import unittest

from recomendador import FILMES, ranking_de_filmes, recomendar_filmes

FAVORITOS = ["Toy Story", "Monsters, Inc."]


class TestRecomendador(unittest.TestCase):
    def test_favorito_escondido_aparece_no_top_3(self):
        self.assertIn("Finding Nemo", recomendar_filmes(FAVORITOS, quantidade=3))

    def test_ordem_esperada_do_exemplo(self):
        self.assertEqual(
            recomendar_filmes(FAVORITOS),
            ["Finding Nemo", "Shrek", "The Incredibles"],
        )

    def test_nao_recomenda_filmes_favoritos(self):
        recomendados = recomendar_filmes(FAVORITOS, quantidade=len(FILMES))
        self.assertFalse(set(FAVORITOS) & set(recomendados))

    def test_resultado_e_deterministico(self):
        primeiro = ranking_de_filmes(FAVORITOS)
        for _ in range(5):
            self.assertEqual(ranking_de_filmes(FAVORITOS), primeiro)

    def test_filme_fora_do_catalogo_gera_erro(self):
        with self.assertRaises(ValueError):
            recomendar_filmes(["Filme que não existe"])


if __name__ == "__main__":
    unittest.main()
