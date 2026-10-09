#!/usr/bin/env python3
"""Validate CIDR entries and report overlapping networks.

Usage:
  python validate_networks.py 10.10.10.0/24 10.20.10.0/24 10.100.0.0/16
"""
from __future__ import annotations

import argparse
import ipaddress
import sys


def parse_networks(values: list[str]) -> list[ipaddress._BaseNetwork]:
    networks = []
    for value in values:
        try:
            networks.append(ipaddress.ip_network(value, strict=False))
        except ValueError as exc:
            raise ValueError(f"Invalid network '{value}': {exc}") from exc
    return networks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cidrs", nargs="+", help="IPv4/IPv6 CIDR prefixes")
    args = parser.parse_args()

    try:
        networks = parse_networks(args.cidrs)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2

    has_overlap = False
    for index, first in enumerate(networks):
        for second in networks[index + 1 :]:
            if first.version == second.version and first.overlaps(second):
                print(f"OVERLAP: {first} <-> {second}")
                has_overlap = True

    if has_overlap:
        print("Validation failed: overlapping prefixes found.")
        return 1

    print("OK: all supplied prefixes are valid and non-overlapping.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
