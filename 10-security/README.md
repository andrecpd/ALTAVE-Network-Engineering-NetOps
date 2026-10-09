# Segurança para automação de redes

- Aplicar menor privilégio a contas de automação.
- Não versionar senhas, tokens, chaves privadas ou arquivos de configuração sensíveis.
- Usar secrets do GitHub ou um cofre corporativo aprovado.
- Revisar diffs antes de aplicar alterações em equipamentos.
- Manter inventários de laboratório separados dos de produção.
- Registrar alterações, aprovações, resultados e rollback.
- Restringir acesso SSH/API por origem e identidade.
- Proteger backups, pois podem conter segredos e topologia sensível.
- Desabilitar execução de produção em workflows de validação genéricos.
- Rotacionar credenciais e revisar permissões regularmente.

Antes de operar em produção, seguir as políticas de segurança e gestão de mudanças da organização.
