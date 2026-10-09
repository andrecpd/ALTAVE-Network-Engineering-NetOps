#!/usr/bin/env python3
"""Validate LAB-01 inventory structure, management IPs, and address plan."""
from __future__ import annotations

import ipaddress
import sys
from pathlib import Path
from typing import Any

import yaml

LAB_DIR = Path(__file__).resolve().parents[1]
INVENTORY_PATH = LAB_DIR / "inventory" / "lab.yml"
VARIABLES_PATH = LAB_DIR / "group_vars" / "all.yml"


class ValidationError(Exception):
    """Raised when lab inventory or address plan is invalid."""


def read_yaml(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
    except OSError as exc:
        raise ValidationError(f"Cannot read {path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise ValidationError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValidationError(f"{path} must contain a YAML mapping")
    return data


def collect_hosts(node: Any, found: dict[str, dict[str, Any]]) -> None:
    if not isinstance(node, dict):
        return
    hosts = node.get("hosts", {})
    if isinstance(hosts, dict):
        for name, variables in hosts.items():
            if name in found:
                raise ValidationError(f"Host '{name}' is defined more than once")
            found[name] = variables if isinstance(variables, dict) else {}
    children = node.get("children", {})
    if isinstance(children, dict):
        for child in children.values():
            collect_hosts(child, found)


def validate() -> list[str]:
    inventory = read_yaml(INVENTORY_PATH)
    variables = read_yaml(VARIABLES_PATH)
    all_group = inventory.get("all")
    if not isinstance(all_group, dict):
        raise ValidationError("Inventory must contain an 'all' group")

    hosts: dict[str, dict[str, Any]] = {}
    collect_hosts(all_group, hosts)
    missing = {"R1", "R2"} - hosts.keys()
    if missing:
        raise ValidationError(f"Missing required router(s): {', '.join(sorted(missing))}")

    seen_ips: dict[str, str] = {}
    for name, attrs in hosts.items():
        address = attrs.get("ansible_host")
        if not address:
            raise ValidationError(f"Host '{name}' is missing ansible_host")
        try:
            normalized = str(ipaddress.ip_address(str(address)))
        except ValueError as exc:
            raise ValidationError(f"Host '{name}' has invalid ansible_host '{address}'") from exc
        if normalized in seen_ips:
            raise ValidationError(
                f"Duplicate host IP {normalized}: {seen_ips[normalized]} and {name}"
            )
        seen_ips[normalized] = name

    raw_networks = variables.get("lab_networks")
    if not isinstance(raw_networks, list) or not raw_networks:
        raise ValidationError("group_vars/all.yml must define a non-empty lab_networks list")

    networks: list[ipaddress._BaseNetwork] = []
    for value in raw_networks:
        try:
            network = ipaddress.ip_network(str(value).split("#", 1)[0].strip(), strict=True)
        except ValueError as exc:
            raise ValidationError(f"Invalid CIDR '{value}': {exc}") from exc
        for prior in networks:
            if network.version == prior.version and network.overlaps(prior):
                raise ValidationError(f"Overlapping prefixes: {prior} and {network}")
        networks.append(network)

    return [
        f"Hosts checked: {len(hosts)}",
        f"Unique host IPs: {len(seen_ips)}",
        f"Non-overlapping CIDRs: {len(networks)}",
    ]


def main() -> int:
    try:
        details = validate()
    except ValidationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    for detail in details:
        print(f"  {detail}")
    print("OK: inventory and address plan are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
