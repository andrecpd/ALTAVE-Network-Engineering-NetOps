# Roteiro de laboratórios NetOps

## LAB-01 — Inventário e auditoria com Ansible + Python (PNETLab)

**Guia completo:** [LAB-01 — Ansible, Python e PNETLab](LAB-01-ansible-python-pnetlab/README.md)

O laboratório inclui inventário multi-dispositivo, variáveis globais e por roteador, role Ansible de auditoria somente leitura para Cisco IOS, validação de IPs/CIDRs com Python, testes unitários e geração local de evidências.

Comece pelo guia do LAB-01 e adapte os endereços de gerenciamento para sua topologia. O exemplo inicial usa dois roteadores IOSv; imagens de appliances não são distribuídas neste repositório. A versão de RouterOS exige adaptar os módulos e o método de conexão.

## Validações anteriores

O validador genérico de prefixos também está disponível:

~~~bash
python 04-python/validate_networks.py 10.10.10.0/24 10.20.20.0/24 10.100.0.0/16
python 04-python/validate_networks.py 10.10.0.0/16 10.10.10.0/24
~~~

O segundo comando deve indicar sobreposição e retornar código de saída diferente de zero.

O playbook inicial de validação local continua disponível:

~~~bash
ansible-playbook -i 03-ansible/inventory/lab.yml 03-ansible/playbooks/validate-lab.yml
~~~

## Próximas etapas

- LAB-02: inventário multi-dispositivo e backups de configuração em laboratório.
- LAB-03: fundamentos de VPN IPsec e validação de conectividade.
- LAB-04: desenho de conectividade AWS e tabelas de rotas.
- LAB-05: simulação de failover e recuperação.
- LAB-06: pipeline com aprovação e plano de rollback.
- LAB-07: métricas, dashboard e alertas.

Os laboratórios de VPN, cloud e monitoramento ainda precisam ser implementados e testados. Não são apresentados como integrações já operacionais.
