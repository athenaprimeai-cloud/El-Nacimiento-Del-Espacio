"""Selector: prioriza ataque, no verdad."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from athena_core.explorer import explore_pressure
from athena_core.protocol import ProtocolStore
from athena_core.selector import select_challenges


class SelectorTests(unittest.TestCase):
    def test_groups_and_determinism(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = ProtocolStore(Path(tmp))
            explore_pressure("¿selector test?", n_candidates=40, store=store)
            r1 = select_challenges(store=store)
            r2 = select_challenges(store=store)
        self.assertEqual(r1.n_input, r2.n_input)
        self.assertEqual(
            [x.hypothesis_id for x in r1.ranked],
            [x.hypothesis_id for x in r2.ranked],
        )
        self.assertEqual(r1.n_group_a + r1.n_group_b + r1.n_group_c, r1.n_input)
        self.assertGreater(r1.n_input, 0)
        # At least some structure
        self.assertTrue(any(s.group == "A" for s in r1.ranked) or r1.n_input < 3)


if __name__ == "__main__":
    unittest.main()
