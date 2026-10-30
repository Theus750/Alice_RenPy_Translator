# Plano de Continuidade do RenLocalizer

Este plano resume o que foi identificado na comparação entre a documentação e o projeto atual e organiza a continuação em ordem segura.

## Já foi fechado nesta etapa

- Criação de um `ConfigManager` básico para carregar e salvar configuração.
- Parametrização do fluxo principal para aceitar caminho do projeto, idioma e cache sem caminho hardcoded.
- Delegação do ponto de entrada legado para o fluxo configurável atual.
- Consolidação das implementações em `core/`, mantendo wrappers de compatibilidade na raiz.
- Migração dos testes para validar diretamente os módulos usados pela CLI.
- Validação de arquivos `.rpy` fonte fora de `game/tl/`.
- Criação do parser de blocos `old/new` em arquivos de tradução e identificação de pendências.
- Deteccao e tratamento de menus nomeados para gerar IDs compativeis com o Ren'Py.
- Suporte a menus, prompts de `renpy.input()`, strings de telas e escapes Ren’Py.

## Próximos passos prioritários

1. Implementar tradução em lotes usando `translation.max_batch_size`.
2. Integrar o parser de `tl/` ao pipeline e reaproveitar traduções existentes.
3. Encapsular o LibreTranslate e preparar engines alternativas.
4. Expandir a validação e o pipeline para `.rpa`, `.rpyc` e `.rpymc`.
5. Adicionar deep scan, runtime hook, relatórios e testes de integração.

## Prioridades registradas anteriormente

1. Consolidar um arquivo `config.json` real com os valores usados pelo projeto.
2. Separar a CLI do fluxo atual em um comando explícito com argumentos claros.
3. Expandir o pipeline para validar a pasta `game/` e preparar saídas dentro de `game/tl/<idioma>/`.
4. Evoluir a camada de tradução para suportar engine selecionável e futuras implementações alternativas.
5. Adicionar testes para a resolução de caminhos e para o carregamento da configuração.

## Batching de traducao

O pipeline atual traduz uma entrada por requisição HTTP. Para jogos grandes, isso gera uma chamada por frase e aumenta muito a latência.

A próxima implementação de performance deve:

- separar entradas já presentes no cache;
- proteger placeholders e escapes em cada entrada antes do envio;
- agrupar entradas pendentes em lotes configuráveis, inicialmente até `100` itens;
- enviar os textos ao engine em uma única requisição por lote;
- associar as respostas na mesma ordem aos `translation_id`;
- atualizar o cache após cada lote concluído;
- repetir lotes que falharem respeitando `max_retries`;
- dividir o lote e tentar entradas individuais como fallback;
- manter o comportamento atual para engines que não suportarem listas.

O batching deve preservar a saída atual: `dialogue.rpy`, `strings.rpy` e o arquivo de idioma não devem depender do tamanho dos lotes.

## Compatibilidade por versao da engine

A pipeline atual e especifica para Ren'Py e foi validada principalmente com Ren'Py 8.5.2.26010301. Ela nao deve declarar compatibilidade ampla com todas as versoes sem testes adicionais.

A compatibilidade deve ser separada por adapters e perfis de engine:

```text
EngineAdapter
└── RenPyAdapter
	├── RenPy7Profile
	└── RenPy8Profile
```

Cada perfil deve controlar, quando necessario:

- deteccao da versao do jogo;
- calculo dos identificadores e hashes de traducao;
- normalizacao e encoding de strings;
- tratamento de menus nomeados;
- regras de parsing de `.rpy`;
- invalidacao e recompilacao de `.rpyc`;
- suporte a arquivos empacotados e compilados.

Ren'Py 7 pode funcionar parcialmente com scripts simples, mas ainda nao esta certificado. A deteccao automatica deve permitir override manual da versao quando os metadados do jogo nao forem suficientes.

## Ordem recomendada

1. Implementar batching no tradutor e no `TranslationPipeline`.
2. Cobrir cache hit, ordem dos resultados, placeholders, retries e fallback individual.
3. Integrar o parser de `tl/` ao pipeline.
4. Implementar engine selecionável e suporte a arquivos compilados/empacotados.
5. Conectar a GUI ao backend e ampliar os testes de integração.

## Ordem recomendada registrada anteriormente

1. Integrar o parser de `tl/` ao pipeline e definir a estratégia de reaproveitamento das traduções existentes.
2. Implementar engine selecionável, começando por encapsular o LibreTranslate atual.
3. Expandir a validação e o pipeline para `.rpa`, `.rpyc` e `.rpymc`.
4. Adicionar deep scan, runtime hook e relatórios.
5. Conectar a GUI ao backend e ampliar os testes de integração.

## Ordem recomendada registrada para compatibilidade

1. Detectar a versao da engine Ren'Py e registrar o perfil selecionado.
2. Extrair a logica especifica de identificadores e encoding para um adapter.
3. Criar testes equivalentes para Ren'Py 7 e Ren'Py 8.
4. Validar `.rpyc` e arquivos empacotados por perfil.

## Interface desktop multiplataforma

A interface planejada deve rodar como aplicativo desktop em Windows e Linux, sem depender de navegador externo.

Arquitetura planejada:

```text
Electron main process
	↓ IPC
React renderer
	↓
Python worker
	↓
TranslationPipeline
```

Requisitos de portabilidade:

- nao usar caminhos Windows hardcoded;
- resolver caminhos com `pathlib` no Python e APIs do Node/Electron no frontend;
- empacotar o worker Python separadamente para cada sistema;
- gerar instalador Windows, como NSIS;
- gerar pacote Linux, como AppImage, `.deb` ou equivalente;
- manter a comunicacao Electron/Python independente do shell do sistema;
- testar leitura, escrita, cache e execucao do pipeline em Windows e Linux;
- manter o LibreTranslate acessivel por HTTP nos dois sistemas.

Electron continua sendo a opcao mais simples para React multiplataforma. O custo e gerar e testar um pacote especifico para cada sistema operacional.