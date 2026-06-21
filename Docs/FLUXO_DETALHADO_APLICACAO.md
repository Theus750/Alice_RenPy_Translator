# Fluxo Detalhado da Aplicacao RenLocalizer

Este documento descreve o fluxo completo da aplicacao: como ela recebe um projeto Ren'Py, prepara a pasta `tl/`, extrai textos, traduz, salva os resultados e gera arquivos auxiliares.

## 1. Entrada do usuario

O usuario pode iniciar o processo por dois caminhos:

```text
GUI
└── run.py

CLI
└── run_cli.py
```

Na GUI, o usuario seleciona:

- Caminho do jogo ou executavel.
- Idioma de origem.
- Idioma de destino.
- Motor de traducao.
- Opcoes extras, como deep scan, leitura de `.rpyc`, proxy e runtime hook.

No CLI, os mesmos dados podem vir por argumentos:

```bash
python run_cli.py "C:\Games\MeuJogo" --target-lang portuguese_brazil --engine google --mode full
```

## 2. Ponte entre front e backend

Na interface grafica, o QML chama metodos Python expostos pelo backend.

```text
src/gui/qml/HomePage.qml
        ↓
src/backend/app_backend.py
        ↓
src/core/translation_pipeline.py
```

O `AppBackend` recebe as acoes da tela e cria/configura o pipeline.

Exemplo conceitual:

```text
Botao "Start Translation"
        ↓
backend.startTranslation()
        ↓
TranslationPipeline.configure(...)
        ↓
PipelineWorker.start()
```

O pipeline roda em background para nao travar a interface.

## 3. Configuracao inicial do pipeline

O pipeline recebe:

- Caminho do projeto.
- Idioma alvo.
- Idioma fonte.
- Motor de traducao.
- Se deve extrair `.rpa`.
- Se deve ler `.rpyc`.
- Se deve executar deep scan.
- Se deve usar proxy.

Ele normaliza o caminho.

Se o usuario selecionar:

```text
C:\Games\MeuJogo\game
```

o pipeline entende que o projeto raiz e:

```text
C:\Games\MeuJogo
```

E a pasta principal do jogo e:

```text
C:\Games\MeuJogo\game
```

## 4. Validacao do projeto

Primeira etapa:

```text
VALIDATING
```

O pipeline verifica:

- O caminho existe.
- Existe uma pasta `game/`.
- Existem arquivos `.rpy`.
- Existem arquivos `.rpyc`.
- Existem arquivos `.rpa`.
- Existem arquivos `.rpymc`, se a opcao estiver habilitada.

Estrutura esperada:

```text
MeuJogo/
└── game/
    ├── script.rpy
    ├── screens.rpy
    ├── images/
    └── audio/
```

Se nao existir `game/`, o processo para.

## 5. Deteccao de arquivos empacotados ou compilados

O pipeline procura:

```text
*.rpa
*.rpyc
*.rpymc
```

### `.rpa`

Arquivos `.rpa` sao arquivos empacotados do Ren'Py.

Se houver `.rpa` e a opcao de extracao estiver ativa, o pipeline tenta extrair o conteudo.

```text
UNRPA
```

Ele usa o adaptador:

```text
src/utils/unrpa_adapter.py
```

### `.rpyc`

Arquivos `.rpyc` sao scripts Ren'Py compilados.

Se nao houver `.rpy`, mas houver `.rpyc`, o pipeline pode:

- Ler diretamente com `rpyc_reader`.
- Decompilar com `unrpyc_adapter`/`rpycdec`.
- Continuar em modo RPYC-only, se habilitado.

### `.rpymc`

Arquivos `.rpymc` tambem podem conter texto compilado/modular.

Quando habilitado, o pipeline tenta extrair textos deles e transformar em entradas traduziveis.

## 6. Preparacao dos textos traduziveis no codigo fonte

Etapa:

```text
GENERATING
```

Antes de gerar ou ler a pasta `tl/`, o pipeline pode ajustar alguns textos no codigo `.rpy` para ficarem traduziveis pelo sistema do Ren'Py.

Exemplos:

```renpy
textbutton "Start" action Start()
```

pode virar:

```renpy
textbutton _("Start") action Start()
```

Outro exemplo:

```renpy
renpy.notify("Game saved")
```

pode virar:

```renpy
renpy.notify(_("Game saved"))
```

Isso ajuda o Ren'Py a reconhecer esses textos como strings traduziveis.

O pipeline evita mexer em:

- Comentarios.
- Variaveis com interpolacao.
- Strings ja dentro de `_()`.
- Expressoes `.format()`.
- Assignments tecnicos.
- Linhas que parecem codigo.

## 7. Criacao ou atualizacao da pasta `tl/`

Depois, o pipeline garante que exista:

```text
game/tl/<idioma>/
```

Exemplo:

```text
game/tl/portuguese_brazil/
```

Se a pasta ainda nao existe, ou se os arquivos fonte foram atualizados, o pipeline gera os arquivos de traducao.

O resultado esperado e algo assim:

```text
game/
└── tl/
    └── portuguese_brazil/
        ├── script.rpy
        ├── screens.rpy
        └── strings.rpy
```

Esses arquivos contem blocos de traducao Ren'Py.

## 8. Formato dos arquivos gerados em `tl/`

Para dialogos e blocos de script:

```renpy
translate portuguese_brazil start_abc123:

    # e "Hello!"
    e ""
```

Ou no formato com `old/new`:

```renpy
translate portuguese_brazil id_abc123:
    old "Hello!"
    new ""
```

Para strings de interface:

```renpy
translate portuguese_brazil strings:

    old "Start"
    new ""

    old "Load"
    new ""
```

Nesse momento, os textos ainda nao estao traduzidos. A pasta `tl/` esta preparada para receber as traducoes.

## 9. Parse dos arquivos `tl/`

Etapa:

```text
PARSING
```

O pipeline usa:

```text
src/core/tl_parser.py
```

Ele le os arquivos dentro de:

```text
game/tl/<idioma>/
```

E coleta as entradas com `new ""` vazio.

Cada entrada vira um objeto interno parecido com:

```text
TranslationEntry
├── original_text
├── translated_text
├── file_path
├── line_number
├── entry_type
├── character
├── context_path
└── translation_id
```

Assim o sistema sabe:

- Qual texto deve traduzir.
- De qual arquivo veio.
- Em qual linha estava.
- Qual e o ID da traducao.
- Se era dialogo, menu, UI ou string.

## 10. Deep scan opcional

Se o usuario habilitar deep scan, o pipeline usa:

```text
src/core/parser.py
src/core/deep_extraction.py
```

Essa etapa procura textos que o sistema padrao do Ren'Py pode nao capturar.

Exemplos:

```renpy
init python:
    item_name = "Magic Sword"
    item_desc = "A blade with ancient power."
```

Ou:

```renpy
$ renpy.notify("You found an item")
```

Quando encontra textos extras, o pipeline cria arquivos adicionais em `tl/<idioma>/`, como:

```text
strings_deepscan.rpy
strings_unrpyc.rpy
```

Esses arquivos tambem seguem o formato:

```renpy
translate portuguese_brazil strings:
    old "Magic Sword"
    new ""
```

## 11. Coleta final das entradas nao traduzidas

Depois do parse normal e do deep scan, o pipeline junta tudo:

```text
all_entries = entradas com new vazio
```

Exemplo:

```text
Start
Load
Hello!
What are you doing?
Magic Sword
A blade with ancient power.
```

Se nao houver nada para traduzir, ele ainda pode gerar:

- `strings.json`.
- Runtime hook.
- Arquivo de ativacao de idioma.
- Relatorios.

## 12. Protecao de sintaxe antes da traducao

Etapa:

```text
TRANSLATING
```

Antes de mandar cada texto para o tradutor, o sistema protege partes sensiveis com:

```text
src/core/syntax_guard.py
```

Exemplo original:

```text
Hello, [player_name]! {b}Welcome{/b}.
```

Pode virar algo protegido:

```text
Hello, ⟦VAR0⟧! ⟦TAG0⟧Welcome⟦TAG1⟧.
```

O tradutor recebe a versao protegida.

Depois da traducao, o sistema restaura:

```text
Ola, [player_name]! {b}Bem-vindo{/b}.
```

Isso impede que o tradutor transforme `[player_name]` em outra coisa ou quebre tags Ren'Py.

## 13. Escolha do motor de traducao

O pipeline usa o `TranslationManager`, que escolhe o motor configurado.

Motores possiveis:

```text
google
deepl
openai
gemini
deepseek
local_llm
libretranslate
pseudo
```

Fluxo:

```text
TranslationEntry
        ↓
TranslationRequest
        ↓
TranslationManager
        ↓
Motor escolhido
        ↓
TranslationResult
```

## 14. Cache e glossario

Antes ou depois da traducao, entram dois mecanismos importantes.

### Cache

Se o texto ja foi traduzido antes, o sistema pode reaproveitar a traducao.

Isso evita:

- Traduzir a mesma frase varias vezes.
- Gastar API desnecessariamente.
- Tornar o processo mais lento.

### Glossario

O glossario garante traducoes preferidas para termos especificos.

Exemplo:

```json
{
  "Save": "Salvar",
  "Load": "Carregar",
  "Preferences": "Preferencias"
}
```

O `output_formatter` aplica essas regras no resultado final.

## 15. Filtro de falsos positivos

Depois da traducao, o sistema verifica se aquilo realmente deveria ser traduzido.

Modulo:

```text
src/core/output_formatter.py
```

Ele evita traduzir:

- Nomes de arquivos: `bg_room.png`.
- Audio: `click.ogg`.
- Codigo: `player.level >= 3`.
- Cores: `#ffffff`.
- Numeros: `123`.
- Variaveis: `[player_name]`.
- Termos tecnicos Ren'Py: `xalign`, `yalign`, `dissolve`, `screen`, `label`.
- Paths e URLs.

Essa etapa reduz chance de crash no jogo.

## 16. Salvamento das traducoes nos arquivos `.rpy`

Etapa:

```text
SAVING
```

O pipeline volta aos arquivos em:

```text
game/tl/<idioma>/
```

E preenche os campos `new`.

Antes:

```renpy
translate portuguese_brazil strings:
    old "Start"
    new ""
```

Depois:

```renpy
translate portuguese_brazil strings:
    old "Start"
    new "Iniciar"
```

Antes:

```renpy
translate portuguese_brazil id_abc123:
    old "Hello!"
    new ""
```

Depois:

```renpy
translate portuguese_brazil id_abc123:
    old "Hello!"
    new "Ola!"
```

Os arquivos sao salvos com escrita segura para evitar corrupcao.

## 17. Geracao do `strings.json`

Depois de salvar os `.rpy`, o pipeline gera:

```text
game/tl/<idioma>/strings.json
```

Esse arquivo e um mapa simples:

```json
{
  "Start": "Iniciar",
  "Load": "Carregar",
  "Hello!": "Ola!"
}
```

Ele e usado principalmente pelo runtime hook para traduzir textos que aparecem dinamicamente durante o jogo.

O pipeline tambem pode adicionar aliases:

- Variantes com espacos normalizados.
- Variantes com reticencias.
- Variantes com hotkeys.
- Variantes sem wrappers.
- Variantes observadas em diagnosticos de runtime.

## 18. Geracao do arquivo de ativacao de idioma

O pipeline cria um arquivo como:

```text
game/zzz_portuguese_brazil_language.rpy
```

Esse arquivo tenta forcar o idioma do jogo para o idioma alvo.

Ele pode definir:

```renpy
define config.language = "portuguese_brazil"
```

E tambem usar `renpy.change_language()` no inicio do jogo.

Objetivo:

- Fazer o jogo abrir ja no idioma traduzido.
- Evitar depender de menu de idioma interno.
- Ajudar patches de traducao nao oficiais.

## 19. Geracao do runtime hook

Se habilitado, o pipeline cria:

```text
game/zzz_renlocalizer_runtime.rpy
```

Esse hook:

- Carrega `strings.json`.
- Intercepta textos em runtime.
- Tenta substituir textos por traducao exata.
- Pode registrar textos nao encontrados.

Ele e especialmente util para:

- Textos dinamicos.
- Textos gerados por Python.
- UI customizada.
- Jogos que nao usam perfeitamente o sistema `translate` do Ren'Py.

Regra importante:

```text
O hook deve preferir exact match e evitar substituicoes parciais perigosas.
```

Assim ele evita quebrar variaveis como:

```text
[GAME.ship.name]
```

## 20. Relatorios de diagnostico

O pipeline tambem gera relatorios em:

```text
game/tl/<idioma>/diagnostics/
```

Eles podem registrar:

- Quantos textos foram extraidos.
- Quantos foram traduzidos.
- Quantos foram ignorados.
- Quais textos pareciam corrompidos.
- Quais placeholders foram recuperados.
- Quais arquivos foram escritos.
- Warnings de cobertura.

Esses relatorios ajudam a revisar a traducao e corrigir bugs.

## 21. Fim do processo

Etapa:

```text
COMPLETED
```

Ao final, a estrutura pode ficar assim:

```text
MeuJogo/
└── game/
    ├── script.rpy
    ├── screens.rpy
    ├── zzz_portuguese_brazil_language.rpy
    ├── zzz_renlocalizer_runtime.rpy
    └── tl/
        └── portuguese_brazil/
            ├── script.rpy
            ├── screens.rpy
            ├── strings.rpy
            ├── strings_deepscan.rpy
            ├── strings.json
            └── diagnostics/
```

## 22. Resumo visual do fluxo

```text
Usuario seleciona projeto
        ↓
GUI ou CLI chama backend
        ↓
Pipeline valida game/
        ↓
Detecta .rpy / .rpyc / .rpymc / .rpa
        ↓
Extrai .rpa se necessario
        ↓
Prepara textos traduziveis com _()
        ↓
Cria ou atualiza game/tl/<idioma>/
        ↓
Le arquivos tl gerados
        ↓
Executa deep scan opcional
        ↓
Coleta entradas com new vazio
        ↓
Protege sintaxe Ren'Py
        ↓
Traduz com motor escolhido
        ↓
Restaura placeholders e tags
        ↓
Aplica glossario e filtros
        ↓
Salva new "traducao"
        ↓
Gera strings.json
        ↓
Gera arquivo de idioma
        ↓
Gera runtime hook
        ↓
Gera diagnosticos
        ↓
Conclui
```

## 23. Fluxo dos dados em alto nivel

```text
Arquivos fonte do jogo
        ↓
Textos extraidos
        ↓
Entradas de traducao
        ↓
Requests para tradutor
        ↓
Resultados traduzidos
        ↓
Arquivos Ren'Py em tl/
        ↓
strings.json + runtime hook
```

## 24. Ponto principal

Sim: a aplicacao primeiro le o jogo e prepara/recria os arquivos de traducao dentro da pasta `tl/<idioma>/`. Depois ela le esses arquivos, traduz os textos pendentes e preenche os campos vazios.

Esse fluxo e importante porque respeita a forma nativa do Ren'Py trabalhar com localizacao.

