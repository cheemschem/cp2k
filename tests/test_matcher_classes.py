import unittest

from matchers import run_matcher


class TextPresenceMatcherTest(unittest.TestCase):
    def test_text_from_test_file_spec(self) -> None:
        result = run_matcher(
            "OT LBFGS\nOT DIIS\n", matcher="TEXT_PRESENT", text="OT DIIS"
        )
        self.assertEqual(result.status, "OK")
        self.assertIsNone(result.error)

    def test_text_not_found(self) -> None:
        result = run_matcher("OT LBFGS\n", matcher="TEXT_PRESENT", text="OT DIIS")
        self.assertEqual(result.status, "WRONG RESULT")
        self.assertEqual(result.error, "Text not found: 'OT DIIS'.\n")

    def test_missing_or_invalid_text(self) -> None:
        for spec in ({}, {"text": ""}, {"text": None}, {"text": 1}):
            with self.subTest(spec=spec):
                result = run_matcher("OT DIIS", matcher="TEXT_PRESENT", **spec)
                self.assertEqual(result.status, "N/A")

    def test_existing_named_matcher(self) -> None:
        self.assertEqual(run_matcher("OT DIIS", matcher="OT_diis_update").status, "OK")
        self.assertEqual(
            run_matcher("OT LBFGS", matcher="OT_diis_update").status,
            "WRONG RESULT",
        )

    def test_text_spec_overrides_named_matcher(self) -> None:
        result = run_matcher("OT LBFGS", matcher="OT_diis_update", text="OT LBFGS")
        self.assertEqual(result.status, "OK")

    def test_absence_matcher_still_works(self) -> None:
        result = run_matcher("OT LBFGS", matcher="NO_TEXT", text="OT DIIS")
        self.assertEqual(result.status, "OK")


if __name__ == "__main__":
    unittest.main()
