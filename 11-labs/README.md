# Roteiro de laboratórios NetOps

## LAB-01 — Validação inicial (disponível)

- Executar o validador de CIDRs em Python.
- Executar o playbook Ansible local de coleta de fatos.
- Rodar o workflow GitHub Actions por push ou pull request.

Exemplos:

```bash
python 04-python/validate_networks.py 10.10.10.0/24 10.20.10.0/24 10.100.0.0/16
python 04-python/validate_networks.py 10.10.0.0/16 10.10.10.0/24
```

O segundo comando deve indicar sobreposição e retornar código de saída diferente de zero.

Para Ansible, instale Ansible e use:

```bash
ansible-playbook -i 03-ansible/inventory/lab.yml 03-ansible/playbooks/validate-lab.yml
```

## Próximas etapas

- LAB-02: inventário multi-dispositivo e backups em laboratório.
- LAB-03: fundamentos de VPN IPsec e validação de conectividade.
- LAB-04: desenho de conectividade AWS e tabelas de rotas.
- LAB-05: simulação de failover e recuperação.
- LAB-06: pipeline com aprovação e plano de rollback.
- LAB-07: métricas, dashboard e alertas.

Os laboratórios de VPN, cloud e monitoramento ainda precisam ser implementados e testados. Não são apresentados como integrações já operacionais.
