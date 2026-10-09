from pathlib import Path

import pytest
import yaml

from netops.collect_facts import load_inventory


def make_inventory(tmp_path: Path, value: object) -> Path:
    path = tmp_path / "inventory.yml"
    path.write_text(yaml.safe_dump(value), encoding="utf-8")
    return path


def test_valid_inventory_defaults(tmp_path: Path) -> None:
    path = make_inventory(tmp_path, {"devices": [{"name": "r1", "host": "192.0.2.10", "device_type": "cisco_ios"}]})
    device = load_inventory(path)[0]
    assert device["port"] == 22
    assert device["enabled"] is True


def test_missing_devices_list_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="devices"):
        load_inventory(make_inventory(tmp_path, {"routers": []}))


def test_duplicate_names_are_rejected(tmp_path: Path) -> None:
    item = {"name": "r1", "host": "192.0.2.10", "device_type": "cisco_ios"}
    with pytest.raises(ValueError, match="duplicado"):
        load_inventory(make_inventory(tmp_path, {"devices": [item, item]}))


def test_invalid_port_is_rejected(tmp_path: Path) -> None:
    item = {"name": "r1", "host": "192.0.2.10", "device_type": "cisco_ios", "port": 70000}
    with pytest.raises(ValueError, match="Porta inválida"):
        load_inventory(make_inventory(tmp_path, {"devices": [item]}))
