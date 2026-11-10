import unittest

from skillpack import expr


class ExprTest(unittest.TestCase):
    def test_arithmetic_and_logic(self):
        env = {"a": 7, "b": 2, "s": "x", "f": False}
        self.assertEqual(expr.evaluate("a - b * 2", env), 3)
        self.assertEqual(expr.evaluate("round(100 * b / a)", env), 29)
        self.assertTrue(expr.evaluate("a >= 7 and not f", env))
        self.assertTrue(expr.evaluate("s == 'x' or a < 0", env))
        self.assertTrue(expr.evaluate("s in ['x', 'y']", env))
        self.assertTrue(expr.evaluate("0 < b < a", env))
        self.assertIs(expr.evaluate("true", {}), True)

    def test_names(self):
        self.assertEqual(expr.names("max(a, b) > c and true"), {"a", "b", "c"})

    def test_rejects_unsafe_constructs(self):
        for source in [
            "__import__('os').system('id')",
            "a.__class__",
            "a[0]",
            "(lambda: 1)()",
            "open('x')",
            "[x for x in a]",
            "a ** 99",
            "f'{a}'",
            "a if b else c",
            "min(a, key=b)",
        ]:
            with self.subTest(source=source):
                with self.assertRaises(expr.ExprError):
                    expr.evaluate(source, {"a": 1, "b": 2, "c": 3})

    def test_errors(self):
        with self.assertRaises(expr.ExprError):
            expr.evaluate("x + 1", {})
        with self.assertRaises(expr.ExprError):
            expr.evaluate("1 / 0", {})
        with self.assertRaises(expr.ExprError):
            expr.evaluate("'a' < 1", {})
        with self.assertRaises(expr.ExprError):
            expr.evaluate("1 +", {})
        with self.assertRaises(expr.ExprError):
            expr.evaluate("1 + " * 200 + "1", {})


if __name__ == "__main__":
    unittest.main()
