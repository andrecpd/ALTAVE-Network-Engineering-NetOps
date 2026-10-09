# Runbook — troubleshooting de VPN site-to-site

## Sintoma: túnel ativo, tráfego indisponível

1. Confirmar estado IKE e IPsec/child SA nas duas pontas.
2. Verificar contadores de bytes/pacotes e tempo de vida das SAs.
3. Confirmar seletores de tráfego/local e remoto.
4. Validar rotas de ida e retorno.
5. Conferir ACL/firewall e NAT exemption, quando aplicável.
6. Validar MTU/MSS e investigar fragmentação.
7. Conferir logs, perda de pacotes e alterações recentes.
8. Fazer teste controlado com origem e destino conhecidos.

## Sintoma: túnel flapping em link instável

- Correlacionar quedas com perda, latência, troca de endereço e eventos do ISP.
- Verificar DPD/keepalive e timers compatíveis entre os peers.
- Validar estabilidade do underlay antes de alterar timers.
- Considerar link secundário e política de failover, se suportados.
- Evitar mudanças simultâneas em criptografia, roteamento e MTU.

## Antes de mudar

- Registrar estado atual e coletar logs.
- Fazer backup seguro da configuração.
- Confirmar acesso fora de banda.
- Definir plano de rollback e critério de sucesso.

## Critérios de recuperação

- SAs estáveis.
- Rotas presentes nos dois sentidos.
- Testes de conectividade aprovados.
- Perda/latência dentro do limite definido para o serviço.
- Alertas resolvidos e incidente documentado.

Comandos específicos variam por fabricante. Execute somente comandos de leitura em produção até haver autorização formal para mudanças.
