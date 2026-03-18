# Projeto Tradução Ren'Py

Pipeline em Python para extrair textos de jogos Ren'Py, traduzir o conteúdo via API HTTP e gerar arquivos de tradução em `game/tl/portuguese/`.

## Visão Geral

Este projeto foi feito para:

- ler arquivos `.rpy` de um jogo Ren'Py
- extrair diálogos, narração e escolhas de menu
- proteger placeholders antes da tradução
- salvar as entradas extraídas em JSON
- gerar arquivos `.rpy` de tradução

O fluxo principal atual está em [translation_pipeline.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/translation_pipeline.py) e [main_dialogue.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/main_dialogue.py).

## Estrutura do Projeto

```text
Projeto_traducao_renpy/
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- cache.json
|-- extracted_entries.json
|-- translation_pipeline.py
|-- translator.py
|-- text_source_parser.py
|-- translation_entry.py
|-- syntax_guard.py
|-- dialogue_output.py
|-- main_dialogue.py
|-- extractor.py
|-- extractor_dialogue.py
|-- generator.py
|-- generator_dialogue.py
|-- generate_strings.py
|-- main.py
|-- test.py
|-- game/
|   `-- tl/
|       `-- portuguese/
|           |-- dialogue.rpy
|           `-- strings.rpy
|-- tests/
|   |-- extracted_entries.json
|   |-- test_text_source_parser.py
|   `-- fixtures/
|       `-- sample_game.rpy
|-- venv/
`-- __pycache__/
```

## Arquivos Principais

- [translation_pipeline.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/translation_pipeline.py): orquestra validação, extração, tradução e gravação da saída.
- [main_dialogue.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/main_dialogue.py): ponto de entrada do pipeline atual.
- [translator.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/translator.py): cliente HTTP para a API de tradução e gerenciamento do `cache.json`.
- [text_source_parser.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/text_source_parser.py): parser de `.rpy`, com extração de diálogos, narração e escolhas.
- [syntax_guard.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/syntax_guard.py): protege placeholders como `[player]`, `{points}` e `%s`.
- [translation_entry.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/translation_entry.py): estrutura das entradas e geração de `translation_id`.
- [dialogue_output.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/dialogue_output.py): gera `game/tl/portuguese/dialogue.rpy`.

## Pastas e Caminhos

### Raiz

- `cache.json`: cache das traduções já processadas.
- `extracted_entries.json`: saída JSON com as entradas extraídas do jogo.
- `requirements.txt`: dependências Python do projeto.

### Saída Ren'Py

- [game/tl/portuguese/dialogue.rpy](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/game/tl/portuguese/dialogue.rpy): blocos `translate portuguese <label>:` com diálogos e narrações.
- [game/tl/portuguese/strings.rpy](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/game/tl/portuguese/strings.rpy): arquivo do fluxo legado de strings.

### Testes

- [tests/test_text_source_parser.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/tests/test_text_source_parser.py): cobre extração, estabilidade de IDs e placeholders.
- [tests/fixtures/sample_game.rpy](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/tests/fixtures/sample_game.rpy): fixture usada nos testes.

### Pastas Locais

- `venv/`: ambiente virtual local.
- `__pycache__/`: cache de bytecode do Python.

## Fluxo Principal

O pipeline atual executa estas etapas:

1. valida o caminho do projeto Ren'Py
2. percorre os arquivos `.rpy`, ignorando a pasta `tl`
3. extrai diálogos, narração e escolhas com contexto de `label` e blocos
4. protege placeholders antes de enviar texto para tradução
5. chama a API HTTP em `http://localhost:5000/translate`
6. restaura os placeholders após a tradução
7. salva as entradas em `extracted_entries.json`
8. gera `game/tl/portuguese/dialogue.rpy`

## Requisitos

- Python 3
- Docker
- Porta `5000` disponível

## Instalação

Crie e ative um ambiente virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

## Docker

# 🐳 LibreTranslate com Docker

Este projeto utiliza o **LibreTranslate** para realizar traduções automáticas de forma local, sem depender de serviços externos.

A maneira recomendada de execução é via **Docker**, garantindo facilidade de setup e portabilidade.

---

# 📦 Requisitos

Antes de começar, você precisa ter instalado:

- Docker
- Porta `5000` disponível

---

# 🚀 Instalação e Execução

## ▶️ Rodar o LibreTranslate

Execute o comando abaixo:

```bash
docker run -p 5000:5000 libretranslate/libretranslate
```

## Observações sobre Docker

- O projeto não possui `Dockerfile` próprio nem `docker-compose.yml` neste repositório.
- O container precisa expor a API em `http://localhost:5000/translate`, que é o endpoint usado por [translator.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/translator.py).
- Se você usar outra porta, outro container ou outro serviço de tradução, ajuste a constante `API_URL` em [translator.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/translator.py).
- Para confirmar que o container está rodando, use `docker ps`.
- Para parar o container, use `docker stop <container_id>` ou `docker stop libretranslate` se tiver definido nome.

## Como Executar

### Pipeline Atual

Em [main_dialogue.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/main_dialogue.py), o caminho do jogo está fixo em:

```python
game_path = r"c:\Users\mathe\OneDrive\Área de Trabalho\jogo_teste\Beachfront-0.4-pc\game"
```

Se você for usar outro projeto Ren'Py, ajuste esse valor antes de executar.

Depois execute:

```powershell
python main_dialogue.py
```

Esse comando:

- carrega o cache existente
- extrai entradas do jogo
- traduz via API
- salva `extracted_entries.json`
- gera `game/tl/portuguese/dialogue.rpy`

### Testes

```powershell
python -m unittest tests\test_text_source_parser.py
```

## Dependências

O projeto atualmente depende de:

```text
requests
```

## Fluxos Legados

O repositório também contém um fluxo mais antigo baseado em scripts separados:

- [main.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/main.py)
- [extractor.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/extractor.py)
- [generator.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/generator.py)
- [generate_strings.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/generate_strings.py)
- [extractor_dialogue.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/extractor_dialogue.py)
- [generator_dialogue.py](/c:/Users/mathe/OneDrive/Área%20de%20Trabalho/Projeto_traducao_renpy/generator_dialogue.py)

Esses arquivos podem ser úteis para referência, mas o fluxo mais consistente hoje é o de `TranslationPipeline`.

## Observações

- O parser ignora arquivos dentro de `tl/` para evitar retraduzir saídas já geradas.
- O arquivo `cache.json` evita retraduções desnecessárias.
- A tradução depende de um serviço HTTP local responder corretamente ao endpoint configurado em `API_URL`.
