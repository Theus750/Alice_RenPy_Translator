# Como Recriar o RenLocalizer Passo a Passo

Este guia descreve uma forma pratica de recriar um projeto semelhante ao RenLocalizer: uma aplicacao Python para extrair, traduzir e gerar arquivos de localizacao para jogos Ren'Py, com GUI, CLI, pipeline central, multiplos motores de traducao e ferramentas auxiliares.

## 1. Defina o objetivo do projeto

Antes de escrever codigo, fixe o escopo principal:

- Ler projetos Ren'Py a partir de uma pasta ou executavel.
- Encontrar textos traduziveis em `.rpy`, `.rpyc`, `.rpymc` e arquivos estruturados.
- Evitar traduzir codigo, caminhos, imagens, nomes tecnicos e placeholders.
- Traduzir com motores externos ou locais.
- Gerar saida compativel com Ren'Py em `game/tl/<idioma>/`.
- Oferecer GUI desktop e CLI.
- Manter cache, glossario, diagnosticos e testes.

## 2. Crie a estrutura inicial

Monte uma estrutura parecida com esta:

```text
RenLocalizer/
├── run.py
├── run_cli.py
├── requirements.txt
├── config.json
├── glossary.json
├── README.md
├── docs/
├── locales/
├── tests/
└── src/
    ├── version.py
    ├── cli_main.py
    ├── backend/
    ├── core/
    ├── gui/qml/
    ├── tools/
    └── utils/
```

Responsabilidades principais:

- `run.py`: inicializador da GUI.
- `run_cli.py`: inicializador do CLI.
- `src/core/`: regras de extracao, traducao e geracao de saida.
- `src/backend/`: ponte entre QML e Python.
- `src/gui/qml/`: interface grafica.
- `src/utils/`: configuracao, encoding, logs, arquivos e utilitarios.
- `src/tools/`: ferramentas opcionais, como lint, fuzzy matching e font check.
- `tests/`: testes unitarios e regressivos.

## 3. Configure o ambiente Python

Use Python 3.10 ou superior.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Crie um `requirements.txt` inicial com:

```text
PyQt6>=6.6,<6.11
aiohttp>=3.11.0
requests>=2.32.0
httpx>=0.27.0
urllib3>=2.2.0
chardet>=5.2.0
charset-normalizer>=3.3.0
openai>=1.30.0
google-genai>=1.0.0
rapidfuzz>=3.9.0
pandas>=2.2.0
openpyxl>=3.1.2
unrpa>=2.3.0
PyYAML>=6.0.1
rpycdec>=0.1.12
fonttools>=4.50.0
rich>=13.7.0
Pillow>=10.4.0
uvloop>=0.19.0; sys_platform != "win32"
```

## 4. Crie o sistema de configuracao

Comece por `src/utils/config.py`.

Ele deve conter:

- Dataclasses para configuracoes.
- Idioma de origem e destino.
- Motor de traducao selecionado.
- Batch size, timeout, retries e concorrencia.
- API keys.
- Configuracoes de proxy.
- Tema e idioma da interface.
- Caminho do ultimo projeto aberto.
- Glossario carregado de `glossary.json`.

Modelo conceitual:

```python
@dataclass
class TranslationSettings:
    selected_engine: str = "google"
    source_language: str = "auto"
    target_language: str = "portuguese_brazil"
    max_batch_size: int = 100
    max_retries: int = 3
    timeout: int = 30
    enable_runtime_hook: bool = True
```

Depois implemente um `ConfigManager` para:

- Carregar `config.json`.
- Validar valores.
- Salvar alteracoes.
- Carregar textos de UI em `locales/<idioma>.json`.
- Carregar e salvar glossario.

## 5. Implemente leitura e escrita segura

Crie `src/utils/encoding.py`.

Objetivo:

- Ler arquivos com `utf-8-sig`, `utf-8` e fallback por `chardet`.
- Escrever arquivos de forma atomica.
- Normalizar `.rpy` para UTF-8 quando necessario.

Isso evita crashes comuns em jogos Ren'Py com arquivos antigos ou encodings mistos.

## 6. Crie o parser Ren'Py-aware

Crie `src/core/parser.py`.

O parser deve:

- Ler `.rpy`.
- Ignorar comentarios e linhas vazias.
- Detectar dialogos.
- Detectar narracao.
- Detectar escolhas de menu.
- Detectar textos de tela, como `text`, `textbutton`, `tooltip`, `label`.
- Detectar chamadas como `renpy.notify("texto")`.
- Ignorar paths, imagens, audio, variaveis, expressoes Python e termos tecnicos.

Crie constantes de tipo de texto:

```python
class TextType:
    DIALOGUE = "dialogue"
    NARRATION = "narration"
    MENU_CHOICE = "menu_choice"
    SCREEN_TEXT = "screen_text"
    UI_ACTION = "ui_action"
```

Comece simples com regex e depois evolua para:

- Analise por indentacao.
- Contexto de blocos.
- Extracao profunda em blocos `init python`.
- Suporte a JSON/YAML.
- Suporte a `.rpyc` e `.rpymc`.

## 7. Crie o Syntax Guard

Crie `src/core/syntax_guard.py`.

Esse modulo e essencial. Ele protege partes que os tradutores nao podem alterar:

- Variaveis Ren'Py: `[player_name]`.
- Tags Ren'Py: `{b}`, `{/b}`, `{color=#fff}`.
- Placeholders Python: `%s`, `%d`, `%(name)s`, `{}`.
- Tokens especiais.
- Ruby/furigana e outros formatos sensiveis.

Fluxo esperado:

```python
protected_text, placeholders = protect_renpy_syntax(text)
translated = translator.translate(protected_text)
final_text = restore_renpy_syntax(translated, placeholders)
```

Tambem implemente validacao:

- Verificar se placeholders voltaram.
- Tentar recuperar placeholders perdidos.
- Corrigir transliteracoes causadas por tradutores.

## 8. Crie os motores de traducao

Crie `src/core/translator.py`.

Defina uma enum:

```python
class TranslationEngine(Enum):
    GOOGLE = "google"
    DEEPL = "deepl"
    OPENAI = "openai"
    GEMINI = "gemini"
    LOCAL_LLM = "local_llm"
    LIBRETRANSLATE = "libretranslate"
    PSEUDO = "pseudo"
```

Crie modelos:

```python
@dataclass
class TranslationRequest:
    text: str
    source_lang: str
    target_lang: str
    engine: TranslationEngine
    metadata: dict = field(default_factory=dict)
```

```python
@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    success: bool
    error: str | None = None
```

Depois crie uma classe base:

```python
class BaseTranslator(ABC):
    @abstractmethod
    async def translate_single(self, request: TranslationRequest) -> TranslationResult:
        ...

    async def translate_batch(self, requests: list[TranslationRequest]) -> list[TranslationResult]:
        return [await self.translate_single(r) for r in requests]
```

Motores recomendados:

- `GoogleTranslator`: usando `aiohttp`, varios endpoints e fallback.
- `DeepLTranslator`: usando API key.
- `LibreTranslateTranslator`: para instancia local ou self-hosted.
- `PseudoTranslator`: para testes.

Crie `src/core/ai_translator.py` para:

- `OpenAITranslator`.
- `GeminiTranslator`.
- `DeepSeekTranslator`.
- `LocalLLMTranslator`.

Nos LLMs, use prompts que obriguem o modelo a preservar placeholders.

## 9. Crie o Translation Manager

Ainda em `translator.py`, crie um gerenciador para:

- Registrar motores disponiveis.
- Escolher motor ativo.
- Aplicar cache.
- Controlar batch.
- Controlar concorrencia.
- Salvar e carregar memoria de traducao.

Exemplo conceitual:

```python
manager.add_translator(TranslationEngine.GOOGLE, GoogleTranslator(...))
result = await manager.translate(request)
```

## 10. Crie o parser de arquivos `tl/`

Crie `src/core/tl_parser.py`.

Ele deve ler arquivos Ren'Py de traducao:

```renpy
translate portuguese id_abc123:
    old "Hello"
    new ""
```

E tambem blocos:

```renpy
translate portuguese strings:
    old "Start"
    new ""
```

O parser deve retornar objetos como:

- `TranslationFile`.
- `TranslationEntry`.
- `translation_id`.
- `original_text`.
- `translated_text`.
- `file_path`.
- `line_number`.

Depois implemente `save_translations()` para preencher os `new ""`.

## 11. Crie o formatador de saida

Crie `src/core/output_formatter.py`.

Responsabilidades:

- Aplicar glossario.
- Preservar capitalizacao.
- Ignorar falsos positivos.
- Bloquear arquivos, paths, cores, numeros, funcoes, variaveis e termos tecnicos.
- Gerar texto seguro para Ren'Py.

Esse modulo e uma defesa extra depois do parser e do syntax guard.

## 12. Crie o pipeline principal

Crie `src/core/translation_pipeline.py`.

Esse e o fluxo central:

```text
VALIDATING
  -> UNRPA
  -> GENERATING
  -> PARSING
  -> TRANSLATING
  -> SAVING
  -> COMPLETED
```

Implemente:

1. Validar se existe pasta `game/`.
2. Detectar `.rpy`, `.rpyc`, `.rpymc` e `.rpa`.
3. Extrair `.rpa` quando necessario.
4. Gerar `game/tl/<idioma>/`.
5. Tornar alguns textos de UI traduziveis com `_()`.
6. Parsear arquivos `tl/`.
7. Fazer deep scan opcional.
8. Traduzir entradas nao traduzidas.
9. Salvar nos arquivos `.rpy`.
10. Gerar `strings.json`.
11. Gerar hook runtime.
12. Gerar relatorios de diagnostico.

Use sinais Qt se quiser integrar com GUI:

```python
class TranslationPipeline(QObject):
    log_message = pyqtSignal(str, str)
    progress_changed = pyqtSignal(int, int, str)
    stage_changed = pyqtSignal(str, str)
    finished = pyqtSignal(object)
```

## 13. Adicione extracao de `.rpa`, `.rpyc` e `.rpymc`

Crie:

- `src/utils/unrpa_adapter.py`.
- `src/utils/unrpyc_adapter.py`.
- `src/core/rpyc_reader.py`.
- `src/core/rpymc_reader.py`.

Use:

- `unrpa` para extrair `.rpa`.
- `rpycdec` como fallback para `.rpyc`.
- Reader proprio quando possivel.

Regra importante: nunca processe pastas internas do motor Ren'Py como `renpy`, `common`, `lib`, `python-packages`, `cache` e `tl` como se fossem conteudo do jogo.

## 14. Crie o runtime hook

Crie `src/core/runtime_hook_template.py`.

Objetivo:

- Gerar um `.rpy` que carrega `strings.json`.
- Aplicar traducao em runtime via mecanismos do Ren'Py.
- Cobrir textos dinamicos que nao entraram nos arquivos `tl/`.

Saida esperada:

```text
game/
├── zzz_<idioma>_language.rpy
└── zzz_renlocalizer_runtime.rpy
```

O hook deve ser conservador:

- Preferir exact match.
- Evitar substituir substrings arbitrarias.
- Nao quebrar variaveis como `[player.name]`.
- Registrar misses em diagnostico quando habilitado.

## 15. Crie o backend da GUI

Crie `src/backend/app_backend.py`.

Ele deve expor slots para QML:

- Selecionar projeto.
- Definir idioma origem/destino.
- Definir motor.
- Iniciar traducao.
- Parar traducao.
- Gerenciar glossario.
- Gerenciar cache.
- Rodar ferramentas.
- Emitir logs, progresso e conclusao.

Exemplo:

```python
class AppBackend(QObject):
    logMessage = pyqtSignal(str, str)
    progressChanged = pyqtSignal(int, int, str)
    translationFinished = pyqtSignal(bool, str)

    @pyqtSlot()
    def startTranslation(self):
        ...
```

Crie tambem `settings_backend.py` para configuracoes visuais e persistentes.

## 16. Crie a interface QML

Crie `src/gui/qml/main.qml`.

Estrutura sugerida:

```text
main.qml
components/
└── NavigationBar.qml
pages/
├── HomePage.qml
├── SettingsPage.qml
├── ToolsPage.qml
├── GlossaryPage.qml
├── CachePage.qml
└── AboutPage.qml
```

Paginas:

- `HomePage`: selecionar projeto, idioma, motor e iniciar traducao.
- `SettingsPage`: API keys, batch, timeout, runtime hook, proxy.
- `ToolsPage`: lint, font check, health check.
- `GlossaryPage`: adicionar/importar/exportar termos.
- `CachePage`: visualizar ou limpar memoria de traducao.
- `AboutPage`: versao e informacoes.

No `run.py`, carregue QML com `QQmlApplicationEngine` e registre os backends como context properties.

## 17. Crie o CLI

Crie `run_cli.py` e `src/cli_main.py`.

O CLI deve suportar:

```bash
python run_cli.py
python run_cli.py "C:\Games\MeuJogo" --target-lang pt --engine google --mode full
python run_cli.py "/path/game" --target-lang es --engine openai --deep-scan
```

Use:

- `argparse` para argumentos.
- `rich` para progresso e tabelas.
- `QCoreApplication` para reaproveitar pipeline Qt sem GUI.

Comandos uteis:

- Traduzir projeto.
- Traduzir pasta `tl/` existente.
- Health check.
- Font check.
- Pseudo-localization.
- Extrair glossario.

## 18. Crie ferramentas auxiliares

Em `src/tools/`, adicione:

- `health_check.py`: verifica estrutura do projeto.
- `renpy_lint.py`: procura erros em saida traduzida.
- `font_helper.py`: testa suporte de fonte ao idioma.
- `fuzzy_matcher.py`: reaproveita traducoes antigas com textos parecidos.
- `context_viewer.py`: mostra contexto das strings.
- `glossary_extractor/`: extrai termos recorrentes.

Essas ferramentas melhoram o fluxo real de localizacao, nao apenas a traducao automatica.

## 19. Crie suporte a glossario e import/export

Crie `src/utils/data_transfer.py`.

Funcionalidades:

- Exportar glossario para JSON.
- Exportar glossario para CSV.
- Exportar glossario para XLSX.
- Importar de JSON/CSV/XLSX.

Use:

- `json` para JSON.
- `pandas` para CSV/Excel.
- `openpyxl` como engine de Excel.

## 20. Crie suporte a fontes

Crie:

- `src/utils/font_injector.py`.
- `src/tools/font_helper.py`.

O font injector deve:

- Mapear idiomas para fontes adequadas.
- Baixar fontes do Google Fonts.
- Copiar arquivos para `game/tl/renlocalizer_fonts/`.
- Gerar `.rpy` para aplicar fonte no jogo.

O font helper deve:

- Ler arquivos de fonte com `fonttools`.
- Verificar se a fonte suporta caracteres do idioma alvo.

## 21. Crie diagnosticos

Crie `src/core/diagnostics.py`.

Registre:

- Textos extraidos.
- Textos traduzidos.
- Textos ignorados.
- Entradas corrompidas.
- Placeholders recuperados.
- Warnings de cobertura.
- Caminhos de arquivos gerados.

Gere relatorios em:

```text
game/tl/<idioma>/diagnostics/
```

## 22. Crie arquivos de idioma da interface

Em `locales/`, crie:

```text
en.json
pt-BR.json
tr.json
de.json
es.json
fr.json
ru.json
zh-CN.json
```

Cada arquivo deve mapear chaves para textos:

```json
{
  "app_title": "RenLocalizer",
  "stage_validating": "Validating project",
  "stage_translating": "Translating",
  "stage_completed": "Completed"
}
```

## 23. Crie testes desde cedo

Use `unittest` ou `pytest`.

Priorize testes para:

- Parser de dialogos.
- Parser de menus.
- Textos de tela.
- Falsos positivos.
- Syntax guard protect/restore.
- Placeholders quebrados.
- Output formatter.
- `tl_parser`.
- Runtime hook.
- `.rpyc` reader.
- Cache.
- Config sanitization.

Exemplo:

```bash
python -m unittest discover tests
```

ou:

```bash
python -m pytest tests/
```

## 24. Crie empacotamento desktop

Use PyInstaller.

Crie `RenLocalizer.spec` com:

- Executavel GUI baseado em `run.py`.
- Executavel CLI baseado em `run_cli.py`.
- Inclusao de `locales/`.
- Inclusao de `src/gui/qml/`.
- Inclusao de `icon.ico` e `icon.png`.
- Hidden imports de PyQt6, aiohttp, requests, httpx, openai, google-genai, yaml, fonttools etc.

Comando:

```bash
pyinstaller RenLocalizer.spec
```

## 25. Ordem recomendada de desenvolvimento

Uma ordem segura para recriar o projeto:

1. Estrutura de pastas.
2. ConfigManager.
3. Encoding seguro.
4. Parser simples de `.rpy`.
5. Syntax guard.
6. Tradutor pseudo.
7. TranslationManager.
8. TL parser.
9. Pipeline basico.
10. CLI minimo.
11. Google translator.
12. Output formatter e false-positive filters.
13. Glossario e cache.
14. GUI QML basica.
15. Deep scan.
16. `.rpa` extraction.
17. `.rpyc` reader/decompiler.
18. AI translators.
19. Runtime hook.
20. Ferramentas auxiliares.
21. Testes regressivos.
22. PyInstaller.

## 26. MVP minimo

Se quiser recriar primeiro uma versao pequena, implemente apenas:

- `run_cli.py`.
- `ConfigManager`.
- `RenPyParser` para `.rpy`.
- `SyntaxGuard`.
- `PseudoTranslator`.
- `GoogleTranslator`.
- `TLParser`.
- `TranslationPipeline`.
- Testes de parser e syntax guard.

Depois adicione GUI, IA, `.rpa`, `.rpyc`, runtime hook e ferramentas.

## 27. Cuidados importantes

- Nunca traduza paths de arquivos.
- Nunca traduza nomes de imagens, audio, transforms ou labels tecnicas.
- Nunca remova placeholders.
- Nunca altere tags Ren'Py.
- Evite substring replacement no runtime hook.
- Sempre escreva `.rpy` em UTF-8 seguro.
- Nao processe a pasta interna do motor Ren'Py.
- Sempre tenha testes para casos que ja quebraram antes.

## 28. Resultado esperado

Ao final, o projeto deve permitir:

```bash
python run.py
```

para abrir a GUI, e:

```bash
python run_cli.py "C:\Games\MeuJogo" --target-lang portuguese_brazil --engine google --mode full
```

para traduzir pelo terminal.

A saida principal deve ficar em:

```text
C:\Games\MeuJogo\game\tl\portuguese_brazil\
```

com arquivos `.rpy`, `strings.json`, hook runtime e diagnosticos.

