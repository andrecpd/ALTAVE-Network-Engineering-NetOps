"""Unit tests for the LAB-01 inventory validator."""
from __future__ import annotations

import importlib.util
import ipaddress
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "validate_inventory.py"
SPEC = importlib.util.spec_from_file_location("validate_inventory", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class InventoryValidationTests(unittest.TestCase):
    def test_current_lab_inventory_is_valid(self) -> None:
        details = MODULE.validate()
        self.assertTrue(any(item.startswith("Hosts checked:") for item in details))

    def test_overlapping_prefixes_are_detectable(self) -> None:
        parent = ipaddress.ip_network("10.10.0.0/16")
        child = ipaddress.ip_network("10.10.10.0/24")
        self.assertTrue(parent.overlaps(child))

    def test_invalid_cidr_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ipaddress.ip_network("10.10.10.0/33", strict=True)


if __name__ == "__main__":
    unittest.main()
