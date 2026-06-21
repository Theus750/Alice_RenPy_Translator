# Plano de Continuidade do RenLocalizer

Este plano resume o que foi identificado na comparação entre a documentação e o projeto atual e organiza a continuação em ordem segura.

## Já foi fechado nesta etapa

- Criação de um `ConfigManager` básico para carregar e salvar configuração.
- Parametrização do fluxo principal para aceitar caminho do projeto, idioma e cache sem caminho hardcoded.
- Delegação do ponto de entrada legado para o fluxo configurável atual.

## Próximos passos prioritários

1. Consolidar um arquivo `config.json` real com os valores usados pelo projeto.
2. Separar a CLI do fluxo atual em um comando explícito com argumentos claros.
3. Expandir o pipeline para validar a pasta `game/` e preparar saídas dentro de `game/tl/<idioma>/`.
4. Evoluir a camada de tradução para suportar engine selecionável e futuras implementações alternativas.
5. Adicionar testes para a resolução de caminhos e para o carregamento da configuração.

## Ordem recomendada

1. Configuração.
2. Entrada de execução.
3. Validação do projeto.
4. Expansão do pipeline.
5. Cobertura de testes.