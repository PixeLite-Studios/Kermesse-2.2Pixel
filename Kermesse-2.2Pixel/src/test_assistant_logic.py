"""Pruebas rápidas de las respuestas locales y la memoria de Kermesse-2.2Pixel."""
import unittest
import numpy as np
import os
import tempfile

from assistant_logic import LocalAssistant
from tokenizer import CharTokenizer, normalize_user_text


class AssistantLogicTests(unittest.TestCase):
    def setUp(self):
        self.logic = LocalAssistant()
        self.rng = np.random.default_rng(7)

    def ask(self, text):
        return self.logic.respond(text, text.lower(), 1200472, self.rng)

    def test_exact_math_and_division_by_zero(self):
        self.assertIn("El resultado es 42.", self.ask("¿Cuánto es 6 por 7?"))
        self.assertIn("El resultado es 9.", self.ask("81 dividido por 9"))
        self.assertIn("El resultado es 125.", self.ask("¿Cuánto es cinco al cubo?"))
        self.assertIn("El resultado es 12.", self.ask("¿Cuánto es 15% de 80?"))
        self.assertIn("El resultado es 9.", self.ask("raíz cuadrada de 81"))
        self.assertIn("El resultado es 14.", self.ask("(2 + 5) * 2"))
        self.assertIn("cero", self.ask("¿cuánto es 8 / 0?"))

    def test_percentage_survives_tokenizer_normalization(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        tok = CharTokenizer.load(os.path.join(root, "data", "vocab.json"))
        raw = "¿Cuánto es 15% de 80?"
        normalized = normalize_user_text(raw, tok)
        self.assertNotIn("%", normalized)
        answer = self.logic.respond(raw, normalized, 1200472, self.rng)
        self.assertIn("El resultado es 12.", answer)

    def test_capital_and_unknown_fact(self):
        self.assertIn("Lima", self.ask("¿Cuál es la capital de Perú?"))
        self.assertIn("prefiero no inventarlo", self.ask("¿capital de Mongolia?"))
        self.assertIn("prefiero no inventar", self.ask("¿Cómo se cocina un risotto?"))

    def test_capital_followup_keeps_the_country_reference(self):
        self.assertIn("Santiago", self.ask("¿cuál es la capital de Chile?"))
        self.assertIn("Bogotá", self.ask("¿y la de Colombia?"))
        self.assertIn("Bogotá", self.ask("¿y la capital?"))

    def test_memory_keeps_accents_and_ignores_questions(self):
        self.ask("vivo en córdoba")
        self.assertIn("Córdoba", self.ask("¿dónde vivo?"))
        self.ask("me gusta dibujar")
        self.assertIn("dibujar", self.ask("¿qué me gusta hacer?"))
        self.assertEqual(self.logic.facts["hobby"], "dibujar")

    def test_reset_erases_short_term_memory(self):
        self.ask("me llamo lucía")
        self.logic.reset()
        self.assertIn("Todavía no", self.ask("¿cómo me llamo?"))

    def test_parameter_claim_is_truthful_and_bounded(self):
        answer = self.ask("¿cuántos parámetros tenés?")
        self.assertIn("1.200.472", answer)
        self.assertIn("2 millones", answer)

    def test_game_result_and_unknown_data_are_safe(self):
        self.ask("jugamos piedra papel o tijera")
        result = self.ask("tijera")
        self.assertRegex(result, r"Elegí (piedra|papel|tijera)")
        self.assertIn("No tengo internet", self.ask("¿quién ganó el mundial de 1986?"))

    def test_engaging_followups_offer_relevant_next_steps(self):
        self.assertIn("adivinanza", self.ask("estoy aburrido"))
        self.assertIn("lista para charlar", self.ask("bien y vos?"))
        self.assertIn("paso pequeño", self.ask("dame ánimo"))

    def test_relationships_are_not_confused_with_user_identity(self):
        self.ask("mi hermana se llama Camila y tiene 30 años")
        self.assertEqual(self.logic.facts.get("nombre"), None)
        self.assertIn("Camila es tu hermana", self.ask("¿quién es Camila?"))
        self.assertIn("Camila es tu hermana", self.ask("¿quién es mi hermana?"))
        self.assertIn("Camila tiene 30 años", self.ask("¿qué edad tiene ella?"))

    def test_creator_is_pixelite(self):
        for q in ("¿quién te creó?", "quién te hizo", "¿quién es tu creador?", "¿tenés creador?", "¿quién creó a Kermesse?"):
            self.assertIn("PixeLite", self.ask(q))
        self.assertIn("PixeLite", self.ask("¿cómo te llamás? ¿quién sos?"))
        self.assertIsNone(self.ask("quién hizo la pizza"))

    def test_memory_persists_locally_and_reset_removes_it(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "memory.json")
            first = LocalAssistant(memory_path=path)
            first.respond("me llamo Lucia", "me llamo lucia", 1200472, self.rng)
            self.assertTrue(os.path.isfile(path))
            second = LocalAssistant(memory_path=path)
            answer = second.respond("¿cómo me llamo?", "¿cómo me llamo?", 1200472, self.rng)
            self.assertIn("Lucia", answer)
            second.reset(clear_saved=True)
            self.assertFalse(os.path.exists(path))


if __name__ == "__main__":
    unittest.main(verbosity=2)
