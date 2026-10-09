# Arquitetura de referência — rede híbrida

## Objetivo

Conectar unidades on-premises distribuídas a serviços hospedados em cloud com segurança, resiliência, observabilidade e mudanças controladas.

## Blocos lógicos

1. **Unidades remotas:** roteador/firewall, LAN local, link primário e, quando disponível, link de contingência.
2. **Conectividade:** túneis IPsec site-to-site, rotas explícitas e monitoramento de estado.
3. **Cloud:** VPC/VNet, sub-redes privadas, tabelas de rotas, controles de segurança e endpoints necessários.
4. **Plano de gestão:** Linux para automação, Git, Ansible, Python e pipelines de validação.
5. **Observabilidade:** métricas de disponibilidade, RTT, perda, jitter, uso de banda e estado dos túneis.

## Plano de endereçamento fictício

| Domínio | Prefixo |
|---|---|
| Unidade A | 10.10.10.0/24 |
| Unidade B | 10.20.10.0/24 |
| VPC de laboratório AWS | 10.100.0.0/16 |
| Gestão de laboratório | 10.200.0.0/24 |

Verifique sobreposição de CIDRs antes de conectar redes. Em projetos reais, o plano deve vir de uma fonte de verdade aprovada.

## Decisões de projeto

- Preferir sub-redes privadas para workloads internos.
- Restringir fluxos por necessidade de negócio e menor privilégio.
- Definir rotas de ida e volta; validar assimetria e propagação.
- Definir limites de MTU/MSS considerando encapsulamento VPN.
- Projetar failover e testar recuperação, não apenas documentá-los.
- Separar plano de gestão do tráfego de produção sempre que possível.
- Evitar que uma falha do sistema de automação derrube a conectividade existente.

## Checklist de validação

- [ ] CIDRs não sobrepostos.
- [ ] Rotas para redes locais e cloud presentes nos dois sentidos.
- [ ] Políticas de firewall limitadas ao necessário.
- [ ] VPN e monitoramento com alertas testados.
- [ ] DNS e resolução de nomes verificados.
- [ ] Procedimento de rollback documentado.
- [ ] Mudanças revisadas e registradas no Git.

## Limites

Este documento é uma arquitetura de referência genérica, não um diagrama da rede real da ALTAVE. Todos os endereços são exemplos reservados para laboratório.
