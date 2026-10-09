# Zonas de segurança e domínios de falha

Este documento descreve princípios de desenho para o laboratório de rede híbrida. Não representa políticas nem controles existentes em qualquer organização específica.

## Zonas sugeridas

| Zona | Exemplos | Acesso esperado |
|---|---|---|
| Usuários/dispositivos | LAN de cada unidade | Somente serviços necessários |
| Aplicações privadas | Sub-redes privadas da cloud | Fluxos explicitamente aprovados |
| Gestão | Runner NetOps, jump host controlado | Administração autenticada e restrita |
| Monitoramento | Coletores, métricas, syslog | Recepção de telemetria autorizada |
| Plano de controle | APIs e interfaces de gestão de rede | Acesso restrito, auditado e protegido |

## Princípios

- **Menor privilégio:** permitir apenas origem, destino, protocolo e porta necessários.
- **Separação de funções:** separar credenciais de execução, aprovação e administração sempre que possível.
- **Gestão fora do caminho de dados:** quando viável, manter console/out-of-band para recuperar dispositivos após falhas de configuração.
- **Segredos protegidos:** usar secret manager ou armazenamento seguro de CI; não commitar segredos.
- **Auditoria:** registrar quem propôs, revisou e executou cada mudança, sem expor segredos nos logs.
- **Mudanças seguras:** aplicar em laboratório ou grupo piloto e definir critérios de rollback antes da execução.

## Domínios de falha a considerar

1. Equipamento de borda da unidade.
2. Última milha e provedor WAN.
3. Caminho de Internet/transporte.
4. Peer, configuração ou chave da VPN.
5. Roteamento e propagação de prefixos.
6. Gateway, tabelas de rotas ou controles de segurança na cloud.
7. DNS e dependências da aplicação.
8. Plataforma de automação ou credenciais.
9. Coletor de métricas, alertas e canal de notificação.

Redundância só reduz risco quando os componentes não compartilham o mesmo domínio de falha. Dois links que usam o mesmo duto, energia, CPE ou operadora podem falhar juntos; verificar a diversidade real.

## Cenários de teste

| Cenário | Sinal a observar | Ação/validação |
|---|---|---|
| Link WAN degradado | RTT, jitter, perda e retransmissões aumentam | Comparar caminho alternativo e impacto na aplicação |
| Túnel IPsec indisponível | Peer/túnel down ou ausência de tráfego | Verificar IKE, rotas, filtros e logs |
| Rota de retorno ausente | Conexão unilateral ou timeout | Conferir rotas e políticas nos dois sentidos |
| MTU inadequada | Pacotes pequenos funcionam, transferências maiores falham | Teste controlado de MTU/PMTUD e revisão de MSS |
| Regra de firewall excessiva | Fluxos inesperados permitidos | Validar teste negativo e reduzir escopo |
| Falha do pipeline | Mudança não validada ou credencial indisponível | Não executar deploy; corrigir pipeline e manter estado atual |
| Falha de monitoramento | Métricas/alertas ausentes | Alertar sobre perda de telemetria e verificar canal secundário |

## Critérios para considerar o desenho pronto

- [ ] Fluxos autorizados e negados foram testados.
- [ ] A perda de cada componente crítico tem detecção e owner.
- [ ] Dependências compartilhadas foram identificadas.
- [ ] Recuperação foi testada, não apenas presumida.
- [ ] Runbooks e rollback foram revisados por outra pessoa.
- [ ] A documentação não contém dados sensíveis nem credenciais.
