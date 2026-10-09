# CI/CD para Network as Code

## Pipeline sugerido

1. Checkout do repositório.
2. Validar sintaxe YAML.
3. Executar Ansible Lint.
4. Executar testes Python.
5. Validar inventários e templates.
6. Publicar os resultados como artefatos de execução.
7. Para implantação real: revisão humana, aprovação de ambiente, backup, janela de mudança, execução controlada e verificação pós-mudança.

## Controles essenciais

- CI não deve possuir credenciais de produção por padrão.
- Não automatize alterações disruptivas em equipamentos reais sem testes e aprovação.
- Use GitHub Environments e secrets para separar permissões.
- Inclua estratégia de rollback e acesso alternativo ao equipamento.
- Prefira mudanças pequenas e reversíveis.
- Registre quem aprovou e qual commit foi implantado.

O workflow atual executa validações estáticas e testes locais; não configura roteadores, VPNs ou recursos cloud.
