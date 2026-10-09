# Networking: roteamento, VLAN, QoS e diagnóstico

## Roteamento

Ao investigar uma falha, verifique:

1. Interface física/lógica e estado do enlace.
2. Endereço e máscara em cada extremidade.
3. Tabela de roteamento e rota mais específica.
4. Adjacências OSPF/BGP, quando usadas.
5. Rota de retorno e possível assimetria.
6. ACL/firewall, NAT e política de segurança.
7. MTU, fragmentação e MSS.
8. Perda, latência e jitter ao longo do caminho.

## VLAN e switching

- Confirme VLAN permitida nas portas trunk.
- Verifique VLAN nativa e consistência entre pontas.
- Confira estado da interface, erros, drops e negociação.
- Valide gateway, ARP/ND e tabela MAC.
- Evite ampliar domínios de camada 2 sem necessidade.

## QoS

Mapeie classes de tráfego a requisitos de negócio. Valide marcação DSCP, filas, policiamento, shaping e congestionamento em cada salto. QoS não cria largura de banda; ela gerencia concorrência durante congestionamento.

## Comandos Linux úteis

```bash
ip -br address
ip route
ip neigh
ping -c 5 10.100.1.10
tracepath 10.100.1.10
ss -tulpn
sudo tcpdump -ni any host 10.100.1.10
```

Execute apenas em sistemas autorizados. Substitua os endereços pelos destinos do seu laboratório.
