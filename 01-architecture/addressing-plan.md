# Plano de endereçamento — laboratório

> Todos os prefixos são exemplos fictícios para laboratório. Antes de usar qualquer plano real, conferir IPAM/inventário corporativo, redes de fornecedores, VPNs e ambientes cloud.

## Prefixos

| Zona | Prefixo | Gateway ilustrativo | Observações |
|---|---|---|---|
| Unidade A — usuários/dispositivos | 10.10.10.0/24 | 10.10.10.1 | LAN do site A |
| Unidade B — usuários/dispositivos | 10.20.10.0/24 | 10.20.10.1 | LAN do site B |
| AWS VPC | 10.100.0.0/16 | N/A | Bloco agregado; gateway gerenciado pela cloud |
| AWS subnet privada A | 10.100.1.0/24 | Gerenciado pela AWS | Workloads privados |
| AWS subnet privada B | 10.100.2.0/24 | Gerenciado pela AWS | Serviços privados |
| Gestão NetOps | 10.200.0.0/24 | 10.200.0.1 | Administração restrita |

Gateways e alocações de hosts são ilustrativos; confirmar comportamento e endereços reservados na plataforma escolhida.

## Regras de alocação

1. Reservar blocos por organização/região/ambiente/site.
2. Manter um registro único de prefixo, finalidade, proprietário, ambiente, gateway e origem da rota.
3. Evitar reutilizar um prefixo em redes que possam ser conectadas no futuro.
4. Verificar sobreposição de CIDR automaticamente em pull requests.
5. Registrar exceções, motivo, responsável e data de revisão.
6. Evitar publicar endereços internos reais em repositórios públicos.

## Matriz de roteamento conceitual

| Origem | Destino | Anúncio/rota esperada | Política |
|---|---|---|---|
| Unidade A | 10.100.1.0/24 e 10.100.2.0/24 | Rota via túnel IPsec ativo | Somente destinos aprovados |
| Unidade B | 10.100.1.0/24 e 10.100.2.0/24 | Rota via túnel IPsec ativo | Somente destinos aprovados |
| VPC AWS | 10.10.10.0/24 e 10.20.10.0/24 | Rotas via mecanismo de conectividade configurado | Sem rotas mais amplas do que o necessário |
| Gestão NetOps | Endereços de gestão aprovados | Caminho de gestão separado/restrito | SSH/API permitidos apenas a partir de fontes autorizadas |

A tabela representa intenção. A implementação depende do tipo de VPN, roteamento estático ou dinâmico, gateway cloud e equipamento de borda.

## Validação

Executar o validador do repositório:

```bash
python 04-python/validate_networks.py 10.10.10.0/24 10.20.10.0/24 10.100.0.0/16 10.200.0.0/24
```

Esperado: nenhuma sobreposição entre os prefixos fornecidos. O bloco da VPC abrange suas sub-redes internas; portanto, não passe simultaneamente VPC agregada e sub-redes filhas para uma checagem de sobreposição, a menos que o script tenha modo hierárquico que reconheça essa relação.

## Revisão antes de conectar ambientes

- [ ] Prefixos conferidos com IPAM.
- [ ] Sobreposição com redes de terceiros avaliada.
- [ ] Rotas de ida e retorno documentadas.
- [ ] Resumo e filtros de rota revisados.
- [ ] Regras de segurança vinculadas aos fluxos necessários.
- [ ] Plano de rollback e owner definidos.
