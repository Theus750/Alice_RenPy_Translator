# Alice — Tradutor Ren'Py

Aplicação para extrair, traduzir e gerar arquivos de tradução para jogos
Ren'Py. Ela combina leitura direta de arquivos de origem e compilados,
extração de arquivos RPA e tradução por um serviço compatível com a API do
LibreTranslate.

## Recursos

- Interface gráfica em PySide6/QML.
- Extração de diálogos, narrações, menus e textos de interface.
- Leitura direta de `.rpy`, `.rpyc` e `.rpymc`.
- Extração automática de `.rpa` usando `unrpa` ou parser nativo.
- Proteção de placeholders, espaços e pontuação.
- Cache separado por projeto.
- Glossário global e glossário de menus.
- Revisão manual das traduções.
- Geração de `dialogue.rpy` e `strings.rpy`.
- Backup e restauração dos arquivos gerados.
- Histórico e relatório da execução.
- UnRen disponível como ferramenta opcional.
- Empacotamento opcional como executável do Windows.

O UnRen não é necessário no fluxo normal de tradução.

## Requisitos

- Python 3.10 ou superior.
- Um serviço de tradução compatível com LibreTranslate.
- Docker apenas se o LibreTranslate for executado localmente em container.
- PyInstaller apenas para gerar o executável do Windows.

## Instalação

Na raiz do projeto, crie um ambiente virtual isolado:

```powershell
python -m venv venv
```

Ative o ambiente virtual no Windows:

```powershell
# PowerShell
.\venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, permita apenas para a sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

No prompt de comando do Windows:

```bat
venv\Scripts\activate.bat
```

No Linux ou macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Com o ambiente ativo, atualize o `pip` e instale as dependências:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Para confirmar que o ambiente está ativo, o terminal exibirá o prefixo
`(venv)` antes do prompt. Para sair:

```powershell
deactivate
```

O diretório `venv/` é local e não precisa ser enviado ao repositório.

## Execução

### Interface gráfica

```powershell
python src\gui\main.py
```

Selecione a pasta do jogo, que deve conter a pasta `game`, valide o projeto e
inicie a tradução.

### Linha de comando

```powershell
python run_cli.py "<caminho-do-projeto>"
```

Para ver as opções disponíveis:

```powershell
python run_cli.py --help
```

## Fluxo de tradução

1. Valida a pasta do projeto.
2. Extrai arquivos `.rpa`, quando existirem.
3. Lê arquivos `.rpy`.
4. Lê `.rpyc` e `.rpymc` quando não há `.rpy` correspondente.
5. Protege placeholders antes da tradução.
6. Usa cache, glossário e o serviço de tradução.
7. Gera os arquivos em `game/tl/portuguese/`.

Os arquivos `.rpa` originais são preservados. A extração nativa aceita RPA-2.0
e RPA-3.0 sem executar o conteúdo do arquivo.

## Textos suportados

O extrator reconhece:

- falas e narrações;
- escolhas e legendas de menu;
- propriedades de tela como `text`, `textbutton`, `label` e `tooltip`;
- chamadas `_()`, `renpy.input()` e `renpy.notify()`;
- textos em blocos `python:` e linhas `$`;
- textos encontrados em arquivos compilados compatíveis.

Textos montados completamente em tempo de execução, literais técnicos e
formatos `.rpyc` incomuns podem exigir revisão manual.

Arquivos-fonte `.rpy` são preferidos quando existe um `.rpyc` correspondente,
evitando traduções duplicadas.

## Arquivos gerados

```text
game/
└── tl/
    └── portuguese/
        ├── dialogue.rpy
        ├── strings.rpy
        └── zzz_alice_language.rpy
```

O cache do projeto fica em `.alice/cache.json`. Backups dos arquivos gerados
ficam em `game/tl/portuguese/.alice-backups/`. Os arquivos `.rpa` originais
não são apagados pela extração integrada.

## UnRen

O UnRen não é obrigatório para o fluxo normal. Ele fica disponível na aba
**Ferramentas** para casos alternativos de descompilação e recursos auxiliares.

Antes de executar uma opção, a aplicação:

- pede confirmação;
- cria um backup;
- registra a saída em log;
- permite cancelar a execução.

## LibreTranslate local com Docker

Para iniciar o LibreTranslate localmente:

```powershell
docker run -p 5000:5000 libretranslate/libretranslate
```

O endpoint padrão da aplicação é:

```text
http://localhost:5000/translate
```

Mantenha o serviço ativo enquanto estiver usando a interface ou a CLI.

## Testes

```powershell
python -m pytest tests -q
```

A suíte cobre parser de textos, placeholders, leitores compilados, RPA,
interface UnRen e fluxo de configuração.

```text
77 testes e 5 subtestes aprovados
```

## Limitações conhecidas

- Textos construídos totalmente em tempo de execução podem não ser detectados.
- Formatos `.rpyc` incomuns podem exigir revisão ou outra ferramenta.
- A qualidade da tradução depende do modelo ou serviço usado pelo
  LibreTranslate.
- Textos de interface ainda podem exigir revisão manual no dashboard.

## Criar executável para Windows

Instale o PyInstaller no ambiente virtual:

```powershell
pip install pyinstaller
```

Gere o executável:

```powershell
powershell -ExecutionPolicy Bypass -File packaging\build_windows.ps1
```

O resultado será criado em `dist\Alice.exe`. A pasta `dist` deve ser
distribuída junto com um serviço de tradução compatível com LibreTranslate.

O executável não inclui o serviço LibreTranslate. Ele deve estar disponível
na porta configurada durante a execução da tradução.

## Licenças

O código próprio deste projeto é distribuído sob a licença MIT. Consulte
o arquivo [LICENSE](LICENSE).

Componentes de terceiros mantêm suas licenças originais, incluindo UnRen,
`unrpa`, PySide6 e os ícones SVG em `src/gui/qml/icons/`. A inclusão deles
não altera ou substitui suas licenças.
