"""Coleta didática somente leitura de dispositivos de rede via SSH/Netmiko."""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

LOG = logging.getLogger("netops")
READ_ONLY_COMMANDS = ("show version", "show ip interface brief")


def load_inventory(path: Path) -> list[dict[str, Any]]:
    """Carrega o inventário YAML e valida os campos básicos antes de conectar."""
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"Não foi possível ler o inventário: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("devices"), list):
        raise ValueError("O inventário precisa conter uma lista 'devices'.")

    devices: list[dict[str, Any]] = []
    names: set[str] = set()
    for index, item in enumerate(data["devices"], start=1):
        if not isinstance(item, dict):
            raise ValueError(f"devices[{index}] deve ser um objeto YAML.")
        missing = [key for key in ("name", "host", "device_type") if not item.get(key)]
        if missing:
            raise ValueError(f"devices[{index}] sem campos obrigatórios: {', '.join(missing)}")
        if item["name"] in names:
            raise ValueError(f"Nome de dispositivo duplicado: {item['name']}")
        names.add(item["name"])
        port = item.get("port", 22)
        if not isinstance(port, int) or not 1 <= port <= 65535:
            raise ValueError(f"Porta inválida no dispositivo {item['name']}.")
        item.setdefault("port", 22)
        item.setdefault("enabled", True)
        devices.append(item)
    return devices


def collect_device(device: dict[str, Any], username: str, password: str) -> dict[str, Any]:
    """Executa comandos de leitura e devolve resultado sem armazenar credenciais."""
    result: dict[str, Any] = {
        "name": device["name"],
        "host": device["host"],
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "status": "failed",
        "commands": {},
    }
    params = {
        "device_type": device["device_type"], "host": device["host"],
        "username": username, "password": password, "port": device["port"],
        "conn_timeout": 10, "auth_timeout": 10, "banner_timeout": 10, "fast_cli": False,
    }
    try:
        with ConnectHandler(**params) as connection:
            for command in READ_ONLY_COMMANDS:
                result["commands"][command] = connection.send_command(command, read_timeout=30)
        result["status"] = "success"
    except NetmikoAuthenticationException:
        result["error"] = "Falha de autenticação SSH; valide usuário e credencial."
    except NetmikoTimeoutException:
        result["error"] = "Timeout; valide rota, ACL, porta e disponibilidade do dispositivo."
    except (OSError, ValueError) as exc:
        result["error"] = f"Falha operacional: {type(exc).__name__}: {exc}"
    except Exception as exc:  # mantém o lote sob controle sem registrar parâmetros sensíveis
        LOG.exception("Falha não esperada ao coletar %s", device["name"])
        result["error"] = f"Falha não esperada: {type(exc).__name__}"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("reports/facts.json"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        devices = load_inventory(args.inventory)
    except ValueError as exc:
        LOG.error("%s", exc)
        return 2

    enabled = [device for device in devices if device["enabled"]]
    if not enabled:
        LOG.error("Nenhum dispositivo habilitado no inventário.")
        return 2
    username, password = os.getenv("NETOPS_USERNAME"), os.getenv("NETOPS_PASSWORD")
    if not username or not password:
        LOG.error("Defina NETOPS_USERNAME e NETOPS_PASSWORD no ambiente local.")
        return 2

    results = []
    for device in enabled:
        LOG.info("Coleta somente leitura: %s (%s)", device["name"], device["host"])
        results.append(collect_device(device, username, password))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    succeeded = sum(item["status"] == "success" for item in results)
    LOG.info("Resultado: %s/%s dispositivos; saída: %s", succeeded, len(results), args.output)
    return 0 if succeeded == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
