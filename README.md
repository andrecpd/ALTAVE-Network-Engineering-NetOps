# ALTAVE Network Engineering & NetOps

> Portfólio técnico demonstrativo de engenharia de redes, automação e confiabilidade para ambientes híbridos.

Este repositório organiza laboratórios e exemplos de **Network as Code (NetOps)** aplicáveis a redes distribuídas conectadas a ambientes on-premises e cloud. O conteúdo é educacional e deve ser validado em laboratório antes de qualquer uso em produção.

## Objetivos

- Padronizar configurações de rede usando Ansible e Git.
- Demonstrar validação automatizada e práticas seguras de CI/CD.
- Documentar conectividade híbrida, VPN IPsec, roteamento e troubleshooting.
- Automatizar verificações com Python.
- Definir indicadores de disponibilidade, desempenho e confiabilidade.

## Arquitetura de laboratório

- Unidade A: LAN `10.10.10.0/24`
- Unidade B: LAN `10.20.10.0/24`
- AWS VPC de exemplo: `10.100.0.0/16`
- Servidor de automação: Linux com Ansible, Python e Git
- Roteadores: RouterOS ou plataforma equivalente; os exemplos de configuração devem ser adaptados ao fabricante e à versão.

Os endereços são fictícios e destinados a laboratório. Não inclua endereços públicos, credenciais, chaves privadas ou dados de clientes neste repositório.

## Estrutura

```text
.
├── 01-architecture/       # topologia, endereçamento e decisões de design
├── 02-networking/          # roteamento, VLAN, QoS e troubleshooting
├── 03-ansible/             # inventário e playbooks de validação
├── 04-python/              # utilitários de validação de redes
├── 05-hybrid-cloud/        # documentação de conectividade cloud
├── 06-vpn-resilience/      # VPN, MTU/MSS, failover e runbooks
├── 07-linux/               # administração e diagnóstico Linux
├── 08-ci-cd/               # qualidade, testes e controle de mudanças
├── 09-monitoring-sre/      # SLI/SLO, alertas e runbooks
├── 10-security/            # segurança e gestão de segredos
├── 11-labs/                # laboratórios passo a passo
└── 12-interview/           # cases e preparação para entrevista
```

## Comece aqui

1. Leia [a arquitetura de referência](01-architecture/README.md).
2. Prepare o ambiente conforme [o guia de laboratório](11-labs/README.md).
3. Execute as validações de Python e Ansible localmente.
4. Revise o [modelo de CI/CD](08-ci-cd/README.md).
5. Consulte os [runbooks de troubleshooting](06-vpn-resilience/runbook.md).

## Ferramentas

- Ansible e Ansible Lint
- Python 3
- Git e GitHub Actions
- Linux
- AWS VPC / VPN; conceitos aplicáveis também a GCP e Azure
- RouterOS ou plataforma enterprise equivalente
- Zabbix, Prometheus e Grafana (integrações documentadas como evolução)

## Segurança operacional

- Comece sempre com inventário de laboratório.
- Use `--check` quando o módulo e o equipamento suportarem modo de verificação.
- Faça backup antes de mudanças.
- Armazene segredos em um gerenciador apropriado ou GitHub Secrets; nunca no código.
- Exija revisão e aprovação para produção.
- Planeje rollback e valide a conectividade fora de banda antes de alterações remotas.
- Os workflows deste repositório validam artefatos; não aplicam configurações a equipamentos de produção.

## Status do projeto

Este é um portfólio em evolução. A automação inicial cobre validação de estrutura e exemplos de laboratório. Integrações reais com RouterOS, cloud, VPN e monitoramento precisam ser configuradas e testadas no ambiente-alvo antes de serem consideradas prontas para produção.

## Autor

André — Engenharia de Redes, Telecomunicações, Cloud e Automação.

---
*Projeto demonstrativo independente, preparado para estudo e discussão técnica. Não representa arquitetura interna, dados ou sistemas da ALTAVE.*
