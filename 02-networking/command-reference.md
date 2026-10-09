# Referência prática de comandos de networking

Complemento do [módulo Networking](README.md). Os comandos são principalmente exemplos de leitura/diagnóstico Cisco IOS e Linux. Confirme a sintaxe na plataforma do seu laboratório.

## 1. Diagnóstico inicial Cisco IOS

~~~text
show clock
show version
show inventory
show ip interface brief
show interfaces
show interfaces counters errors
show logging
show running-config
~~~

Use show running-config com cuidado ao compartilhar a saída: pode conter endereços, nomes, hashes de senha ou dados operacionais. Redija informações sensíveis antes de anexar evidências.

## 2. Switching

~~~text
show vlan brief
show interfaces status
show interfaces trunk
show mac address-table dynamic
show spanning-tree
show spanning-tree vlan 10
show interfaces <INTERFACE> switchport
~~~

Se um endpoint não alcança outro endpoint na mesma VLAN, confirme link, VLAN access, trunk, VLANs permitidas, tabela MAC, STP e ARP. Não comece alterando roteamento se o tráfego deveria permanecer na mesma VLAN.

## 3. IPv4 e rotas

~~~text
show ip interface brief
show ip route
show ip route <DESTINO>
show arp
ping <DESTINO>
traceroute <DESTINO>
~~~

No Linux:

~~~bash
ip -br address
ip route
ip route get <DESTINO>
ip neigh
ping -c 5 <DESTINO>
tracepath <DESTINO>
~~~

Se existe rota, mas o ping falha, confira caminho de retorno, ACL/firewall, política de ICMP, NAT, VRF, MTU e se o destino está ativo. Ping bloqueado não significa necessariamente falha da aplicação.

## 4. OSPF

~~~text
show ip ospf neighbor
show ip ospf interface brief
show ip ospf database
show ip protocols
show ip route ospf
~~~

| Sintoma | Verificações prioritárias |
|---|---|
| Sem vizinho | IP/máscara, interface, área, protocolo 89, ACL, autenticação |
| EXSTART/EXCHANGE persistente | MTU e parâmetros de interface |
| Vizinho FULL, rota ausente | Origem do prefixo, LSDB, filtros, área, sumarização |
| Rota presente, tráfego falha | Next-hop, retorno, ACL, VRF, MTU |

## 5. BGP

~~~text
show ip bgp summary
show ip bgp
show ip bgp neighbors
show ip route bgp
show running-config | section router bgp
~~~

| Sintoma | Verificações prioritárias |
|---|---|
| Idle/Active | Reachability, TCP/179, peer, ACL, source interface |
| Established, sem prefixo | AFI/SAFI, políticas, filtros, prefixos recebidos |
| Prefixo recebido, não instalado | Next-hop, melhor caminho, RIB e política |
| Prefixo não anunciado | Política de exportação, origem, filtros |

## 6. ACL e fluxo

Antes de editar uma ACL, escreva uma matriz simples:

| Origem | Destino | Protocolo/porta | Esperado | Resultado |
|---|---|---|---|---|
| PC-A | Gateway Site A | ICMP | Permitir | Preencher |
| PC-A | Servidor Site B | TCP/porta do serviço | Conforme política | Preencher |
| VLAN gestão | SSH dos roteadores | TCP/22 | Permitir | Preencher |
| VLAN usuários | SSH dos roteadores | TCP/22 | Negar | Preencher |

Confirme interface, direção, ordem de avaliação e contadores. Não use permit ip any any como correção permanente de troubleshooting.

## 7. QoS e interfaces

~~~text
show interfaces
show policy-map interface
show class-map
show policy-map
~~~

Disponibilidade dos comandos depende da plataforma e da imagem. Observe utilização, drops, erros e contadores de classe antes de concluir que QoS é a causa. Uma política pode estar configurada, mas não aplicada à interface correta.

## 8. Captura e testes Linux

~~~bash
ss -tulpn
dig <NOME>
curl -v --connect-timeout 5 https://<HOST>
sudo tcpdump -ni any host <IP>
~~~

Capture apenas em ambientes autorizados. PCAPs e logs podem conter informações sensíveis; armazene-os em local protegido e redija-os antes de compartilhar.

## 9. Modelo de evidência de incidente

~~~text
INCIDENTE:
Data/hora e fuso:
Impacto:
Escopo:
Mudanças recentes:
Hipótese inicial:
Comandos executados:
Resultados observados:
Causa raiz confirmada:
Ação corretiva:
Validação pós-correção:
Rollback disponível:
Ação preventiva / responsável:
~~~

Um bom relatório separa fatos observados de hipóteses. Registre saída relevante, timestamps e mudanças feitas; não declare causa raiz apenas com base em correlação.
