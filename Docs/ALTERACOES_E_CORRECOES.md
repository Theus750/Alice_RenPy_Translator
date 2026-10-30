# Alteracoes e Correcoes do RenLocalizer

Este documento registra as alteracoes feitas durante a validacao do pipeline com o jogo de teste Ren'Py e a versao Ren'Py 8.5.2.26010301.

## Resumo

O projeto agora:

- usa `core/` como implementacao oficial;
- mantem wrappers na raiz para compatibilidade;
- extrai dialogos, narracoes, menus, prompts e strings de telas;
- gera identificadores compativeis com o algoritmo do Ren'Py;
- preserva placeholders e escapes Ren'Py;
- gera `dialogue.rpy` e `strings.rpy` com entradas aplicaveis pelo Ren'Py;
- possui cobertura automatizada para os casos corrigidos.

## Consolidacao do projeto

A implementacao foi centralizada em `core/`:

- `core/config_manager.py`
- `core/dialogue_output.py`
- `core/syntax_guard.py`
- `core/text_source_parser.py`
- `core/tl_parser.py`
- `core/translation_entry.py`
- `core/translation_pipeline.py`
- `core/translator.py`

Os arquivos equivalentes na raiz passaram a ser wrappers de compatibilidade. A CLI continua em `cli/run_cli.py`, com entrada principal em `run_cli.py`.

O fluxo antigo em `legacy/` foi removido. Saidas geradas, como `extracted_entries.json` e arquivos de traducao locais, podem ser recriadas pelo pipeline e nao fazem parte do nucleo versionado.

## Correcoes do parser

### Placeholders no inicio da fala

**Problema:** textos iniciados por `[player_name]` eram descartados como falsos positivos.

**Causa:** `_is_false_positive()` rejeitava qualquer string iniciada por `[`.

**Correcao:** placeholders no inicio agora sao aceitos. Regras para codigo, comentarios e expressoes iniciadas por `$` ou `#` continuam protegidas.

### Titulos de menu

**Problema:** um titulo como:

```renpy
menu:
    "Who do you apply sunscreen to first?"
```

era classificado como narracao e ia para `dialogue.rpy`.

**Correcao:** titulos de menu sao classificados como `menu_caption` e gerados em `strings.rpy`:

```renpy
old "Who do you apply sunscreen to first?"
new "Para quem voce aplica protetor solar primeiro?"
```

Opcoes de menu continuam sendo classificadas como `menu_choice`.

### Prompts de `renpy.input`

**Problema:** textos usados em `renpy.input()` nao eram extraidos.

**Correcao:** o parser reconhece prompts como:

```renpy
$ player_name = renpy.input("What is your name (default is Alan)?")
```

Esses textos sao classificados como `input_string` e gerados em `strings.rpy`.

### Strings de telas

**Problema:** textos dentro de `screens.rpy`, como botoes do menu inicial, nao eram encontrados porque o parser priorizava scripts dentro de labels.

**Correcao:** strings explicitas com `_()` em telas sao classificadas como `screen_string` e geradas em `strings.rpy`.

Exemplos cobertos:

- `Start`
- `Load`
- `Preferences`
- `Main Menu`
- `Quit`
- `About`
- `Help`
- `Window`
- `Fullscreen`

## Correcoes de traducao e escapes

### Aspa ASCII extra no final

**Problema:** algumas respostas do motor terminavam com uma aspa ASCII extra quando o original usava uma aspa tipografica, por exemplo `”`.

**Correcao:** o pipeline normaliza uma aspa ASCII terminal desequilibrada antes de salvar a traducao. A regra vale para traducoes novas e valores recuperados do cache.

### Escapes Ren'Py

**Problema:** textos com `\\n` eram enviados ao tradutor como texto comum. O resultado podia conter `Nao.` indevido ou sair como `\\\\n` no arquivo gerado.

**Correcao:**

- `\\n`, `\\r` e `\\t` sao protegidos antes da traducao;
- os escapes sao restaurados depois;
- o encoder de saida preserva escapes existentes sem duplica-los.

Resultado esperado:

```renpy
centered "\\n\\nNa manha do segundo dia, todos voces decidem ir juntos a praia."
```

## Identificadores de traducao Ren'Py

### Problema dos menus nomeados

O Ren'Py usa o nome de um menu nomeado no identificador da unidade de traducao.

Para este trecho:

```renpy
menu mc_reaction:
    "Say yes":
        mc "..."
```

O Ren'Py espera um identificador como:

```text
mc_reaction_13e3ba6c
```

O gerador usava incorretamente o label externo, por exemplo:

```text
d6beach2_13e3ba6c
```

**Correcao:** `_label_from_context()` agora prefere o nome do menu quando existe. Menus sem nome continuam usando o label externo.

Essa foi a causa raiz das falas apos escolhas aparecerem em ingles mesmo com traducoes presentes no arquivo.

### Deteccao automatica

O parser agora expoe `find_named_menus()`, que identifica menus nomeados com:

```renpy
menu nome_do_menu:
```

Cada ocorrencia informa arquivo, linha e nome. O pipeline registra esses menus no log antes da extracao, por exemplo:

```text
2 menus nomeados detectados: mc_reaction, pussy_choice
```

Quando um menu nomeado e detectado, o nome e usado automaticamente nos identificadores do menu e das falas posteriores no mesmo contexto Ren'Py.

### Espacos repetidos no hash

**Problema:** o arquivo fonte continha dois espacos antes de `joins`, mas o Ren'Py normalizou esse trecho ao criar o identificador. O projeto gerava `introduction_640493eb`, enquanto o Ren'Py procurava `introduction_bdea9ca6`.

**Correcao:** espacos consecutivos sao normalizados apenas durante o calculo do hash do identificador. O texto original e a traducao nao sao alterados.

## Validacao do projeto Ren'Py

O pipeline agora tambem:

- exige a existencia da pasta `game/`;
- exige ao menos um arquivo `.rpy` fora de `game/tl/`;
- ignora arquivos de traducao ao extrair fontes;
- gera saidas dentro de `game/tl/<idioma>/`;
- permite ler blocos `old/new` com `core/tl_parser.py`;
- identifica blocos pendentes com `new ""`.

## Jogo de teste

Foi adicionado temporariamente ao `screens.rpy` do jogo de teste um painel no menu inicial com:

- botao `Portugues` usando `Language("portuguese")`;
- botao `English` usando `Language(None)`;
- indicador `Active: [preferences.language]`.

O painel serve para diagnosticar o idioma ativo em runtime. Ele pode ser removido depois da validacao.

Bytecodes antigos usados durante os testes foram removidos quando necessario:

- `game/script.rpyc`
- `game/screens.rpyc`
- `game/zzz_renlocalizer_language.rpyc`
- `game/tl/portuguese/dialogue.rpyc`
- `game/tl/portuguese/strings.rpyc`

O Ren'Py recompila esses arquivos ao abrir o jogo.

## Testes

A suite atual pode ser executada com:

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests -q
```

Resultado validado apos as ultimas correcoes:

```text
Ran 32 tests in ...s
OK
```

Os testes cobrem:

- extracao de dialogos e narracoes;
- placeholders no inicio da fala;
- escapes `\\n`;
- menus e titulos de menu;
- prompts de `renpy.input()`;
- strings de telas;
- identificadores de menus nomeados;
- geracao de `dialogue.rpy` e `strings.rpy`;
- configuracao e caminhos;
- cache e normalizacao de traducoes.

## Execucao para validacao

Regenerar as traducoes:

```powershell
.\venv\Scripts\python.exe run_cli.py ".\jogo_teste\Beachfront-0.7-pc"
```

Depois abrir o executavel dentro de `jogo_teste/Beachfront-0.7-pc`, selecionar `Portugues` no painel temporario e iniciar um jogo novo.

No menu de desenvolvedor do Ren'Py, `Shift+D` permite abrir `Show Translation Info`. Essa tela mostra:

- identificador da fala;
- arquivo fonte;
- unidade de traducao encontrada;
- idioma ativo.

## Referencia do Ren'Py

A documentacao oficial consultada foi:

- https://www.renpy.org/doc/html/translation.html
- https://www.renpy.org/doc/html/screen_actions.html

Pontos confirmados na documentacao:

- o idioma primario e representado internamente por `None`;
- idiomas alternativos usam nomes como `portuguese`;
- `Language("portuguese")` altera o idioma em runtime;
- `config.language` define o idioma padrao de inicializacao;
- menus e strings `_()` sao gerados em `translate <idioma> strings:`;
- unidades de dialogo usam o label ou o menu nomeado e um hash do conteudo.
