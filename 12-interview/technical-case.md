# Case técnico — automação de uma rede híbrida distribuída

## Cenário

Uma organização possui várias unidades on-premises conectadas a workloads em cloud por VPN IPsec. O time opera equipamentos de múltiplos fabricantes e precisa reduzir mudanças manuais sem comprometer disponibilidade.

## Abordagem proposta

1. Descobrir e documentar a topologia e os fluxos críticos.
2. Criar uma fonte de verdade para inventário, endereçamento e função de cada equipamento.
3. Classificar configurações por fabricante, versão e ambiente.
4. Implementar roles Ansible idempotentes e tarefas de leitura antes das de mudança.
5. Validar sintaxe, lint, templates e resultados esperados no CI.
6. Testar mudanças em laboratório ou ambiente canário.
7. Exigir aprovação, backup e janela de mudança para produção.
8. Executar verificações pós-mudança e manter rollback testado.
9. Monitorar SLI/SLO, incidentes e mudanças com falha.
10. Evoluir gradualmente para maior cobertura automatizada.

## Como medir sucesso

- Redução do tempo para provisionar uma unidade.
- Menor taxa de erro de configuração.
- Maior cobertura de backup e auditoria.
- Menor MTTR e menos mudanças com falha.
- Maior visibilidade de latência, perda e disponibilidade.

## Perguntas de aprofundamento

- Como tratar diferenças entre RouterOS, Cisco e Juniper?
- Como evitar lockout ao mudar firewall ou rotas remotamente?
- Como validar retorno e simetria do roteamento?
- Como proteger segredos e backups?
- Como testar playbooks sem equipamento físico?
- Como decidir se uma mudança pode ser automatizada sem aprovação manual?

Ao apresentar este case, diferencie claramente experiência comprovada, conhecimento técnico e implementações feitas em laboratório.
