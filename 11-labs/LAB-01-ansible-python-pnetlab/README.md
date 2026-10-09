# LAB-01 — Inventário e auditoria de rede com Ansible e Python

**Objetivo:** construir uma rede de laboratório no PNETLab, validar endereçamento com Python e coletar informações dos roteadores com Ansible, sem aplicar mudanças de configuração.

> Laboratório educacional e independente. IPs e nomes são exemplos, não representam a rede real da ALTAVE. Não conecte este laboratório a redes de produção.

## O que você vai praticar

- Topologia de dois sites no PNETLab.
- Inventário multi-dispositivo e variáveis por grupo/host.
- Ansible com conexão SSH/CLI para Cisco IOS.
- Role reutilizável de auditoria somente leitura.
- Validação de endereços IP e sobreposição de CIDRs com Python.
- Testes unitários, evidências de execução e troubleshooting.

## Compatibilidade

O caminho principal usa Cisco IOSv/IOSvL2 ou appliance IOS compatível com a coleção cisco.ios. As imagens não são distribuídas neste repositório; use somente imagens às quais você tenha direito de acesso. Para MikroTik CHR/RouterOS, a topologia serve como referência, mas os módulos e a conexão Ansible precisam ser adaptados.

## 1. Monte a topologia no PNETLab

Crie os nós:

| Nó | Tipo sugerido | Função |
|---|---|---|
| R1 | Cisco IOSv | Roteador do Site A |
| R2 | Cisco IOSv | Roteador do Site B |
| SW1 | Cisco IOSvL2 | Switch do Site A |
| SW2 | Cisco IOSvL2 | Switch do Site B |
| PC-A | VPCS | Endpoint do Site A |
| PC-B | VPCS | Endpoint do Site B |
| NETOPS | Ubuntu Server ou outra VM Linux | Controlador Ansible/Python, opcional dentro do PNETLab |

Topologia lógica:

~~~text
 PC-A -- SW1 -- R1 ===== link roteado de laboratório ===== R2 -- SW2 -- PC-B
                  |                                      |
                  +---------- rede de gerenciamento -----+
                                  |
                           NETOPS (Linux)
~~~

### Plano de endereçamento de exemplo

| Segmento | Prefixo | Endereços sugeridos |
|---|---|---|
| Gerência | 192.168.100.0/24 | R1 .11, R2 .12, NETOPS .100 |
| LAN Site A | 10.10.10.0/24 | Gateway .1, PC-A .10 |
| LAN Site B | 10.20.20.0/24 | Gateway .1, PC-B .10 |
| Link R1–R2 | 10.255.0.0/30 | R1 .1, R2 .2 |

A rede de gerenciamento só funcionará se houver interface e caminho IP alcançáveis pelo controlador. Não presuma que a rede management do PNETLab seja automaticamente alcançável por todos os nós. Se necessário, use uma interface de laboratório dedicada e documente o caminho.

## 2. Prepare o controlador Linux

Em Debian/Ubuntu:

~~~bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git openssh-client
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r 11-labs/LAB-01-ansible-python-pnetlab/requirements.txt
ansible-galaxy collection install -r 11-labs/LAB-01-ansible-python-pnetlab/requirements.yml
~~~

Verifique as ferramentas:

~~~bash
python --version
ansible --version
ansible-galaxy collection list
ssh -V
~~~

## 3. Configure os roteadores

Configure interfaces, endereços de gerenciamento e SSH conforme a versão do IOSv. Crie um usuário local exclusivo para o laboratório, habilite SSH v2 e restrinja o acesso VTY ao segmento de gerenciamento. Os comandos exatos variam entre imagens.

Checklist por roteador:

- [ ] Interface de gerenciamento endereçada e ativa.
- [ ] Rota de retorno para o controlador configurada.
- [ ] Usuário local exclusivo para o laboratório.
- [ ] SSH habilitado e Telnet desabilitado.
- [ ] Acesso VTY restrito ao controlador, quando possível.
- [ ] Senha exclusiva, sem reutilizar credenciais pessoais/corporativas.
- [ ] Configuração inicial salva e procedimento de restauração conhecido.

Teste a partir do controlador:

~~~bash
ping -c 3 192.168.100.11
ssh labops@192.168.100.11
~~~

Repita para R2. Se ICMP estiver bloqueado por desenho, valide a rota e a porta TCP/22 com ferramenta apropriada, por exemplo netcat. Não desative a validação de chave SSH globalmente; confirme a identidade do equipamento antes de alterar known_hosts.

## 4. Estrutura dos arquivos

~~~text
11-labs/LAB-01-ansible-python-pnetlab/
├── README.md
├── requirements.txt
├── requirements.yml
├── inventory/lab.yml
├── group_vars/all.yml
├── host_vars/R1.yml
├── host_vars/R2.yml
├── playbooks/audit-routers.yml
├── roles/network_audit/defaults/main.yml
├── roles/network_audit/tasks/main.yml
├── tools/validate_inventory.py
├── tests/test_validate_inventory.py
└── artifacts/.gitkeep
~~~

- inventory: grupos e endereços de acesso.
- group_vars: variáveis compartilhadas e redes do cenário.
- host_vars: atributos específicos de cada roteador.
- roles/network_audit: auditoria reutilizável e somente leitura.
- tools: validador local de inventário/CIDRs.
- artifacts: evidências geradas localmente; não inclua segredos.

## 5. Etapa A — Validar inventário e endereçamento

Execute na raiz do repositório:

~~~bash
python 11-labs/LAB-01-ansible-python-pnetlab/tools/validate_inventory.py
~~~

Resultado esperado: mensagem OK e código de saída 0. O script verifica a estrutura YAML, presença de R1/R2, endereços IP duplicados e sobreposição entre os prefixos listados em group_vars/all.yml.

### Teste negativo

Edite temporariamente um prefixo para que ele se sobreponha a outro, execute novamente e confirme que o script reporta a falha e retorna código diferente de zero. Reverta a edição após o teste.

## 6. Etapa B — Validar o inventário Ansible

~~~bash
ansible-inventory -i 11-labs/LAB-01-ansible-python-pnetlab/inventory/lab.yml --graph
ansible-inventory -i 11-labs/LAB-01-ansible-python-pnetlab/inventory/lab.yml --list
ansible-playbook -i 11-labs/LAB-01-ansible-python-pnetlab/inventory/lab.yml 11-labs/LAB-01-ansible-python-pnetlab/playbooks/audit-routers.yml --syntax-check
~~~

O syntax-check não conecta aos equipamentos. Confirme que R1 e R2 aparecem no grupo routers e que os endereços correspondem ao seu PNETLab.

## 7. Etapa C — Executar auditoria somente leitura

O playbook executa consultas no IOS e grava a saída localmente. Ele não aplica configurações.

~~~bash
ansible-playbook \
  -i 11-labs/LAB-01-ansible-python-pnetlab/inventory/lab.yml \
  11-labs/LAB-01-ansible-python-pnetlab/playbooks/audit-routers.yml \
  --ask-pass
~~~

Use o usuário SSH definido no inventário e a senha exclusiva do laboratório quando solicitada. Não coloque senhas nos arquivos versionados. Se seu método de autenticação for diferente, adapte as variáveis de conexão.

Comandos coletados por padrão:

- show version
- show ip interface brief
- show ip route

Confira os arquivos artifacts/R1-audit.txt e artifacts/R2-audit.txt. As evidências são locais e não devem ser commitadas se contiverem dados sensíveis.

## 8. Etapa D — Testes unitários

~~~bash
python -m unittest discover -s 11-labs/LAB-01-ansible-python-pnetlab/tests -v
~~~

## 9. Troubleshooting

| Sintoma | Possível causa | Verificação |
|---|---|---|
| Timeout SSH | Rota, interface ou ACL incorreta | Ping/rota, porta TCP/22 e interfaces no PNETLab |
| Authentication failed | Usuário, senha ou método incorreto | Teste SSH interativo e confirme usuário local |
| Host key changed | Appliance recriado e chave mudou | Verifique a identidade antes de atualizar known_hosts |
| network_os inválido | Coleção ou variável incorreta | Instale requirements.yml e confira ansible_network_os |
| Comando IOS não reconhecido | Imagem/versão diferente | Teste na CLI e ajuste a lista de consultas |
| CIDRs sobrepostos | Prefixos se interceptam | Corrija o plano de endereçamento |
| Sem arquivos de evidência | Playbook falhou antes da gravação | Leia a saída do Ansible e execute a partir da raiz |

## 10. Critérios de conclusão

- [ ] Topologia montada e documentada.
- [ ] Controlador alcança R1 e R2 por SSH.
- [ ] Validador Python passa no cenário válido.
- [ ] Teste negativo de sobreposição falha como esperado.
- [ ] Inventário Ansible mostra os hosts esperados.
- [ ] Playbook passa no syntax-check.
- [ ] Auditoria é executada sem alterar configurações.
- [ ] Evidências de R1 e R2 são geradas localmente.
- [ ] Testes unitários passam.
- [ ] README registra as imagens/versões utilizadas e os problemas encontrados.

## 11. Como apresentar na entrevista

Explique que separou inventário, variáveis e lógica reutilizável; validou o endereçamento antes de executar; começou com automação read-only; registrou evidências e considerou falhas de autenticação, conectividade e compatibilidade. Auditoria não é mudança de configuração: mudanças exigem revisão, backup, plano de rollback e janela aprovada.

## Próxima evolução

1. Adicionar um terceiro roteador e grupos por site.
2. Criar adaptador específico para MikroTik CHR/RouterOS.
3. Validar estado de interfaces e vizinhanças de roteamento.
4. Integrar lint e testes no GitHub Actions.
5. Criar LAB-02 de backup de configuração com retenção e proteção de segredos.
