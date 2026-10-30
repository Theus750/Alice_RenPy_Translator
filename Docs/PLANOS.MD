# RenLocalizer — Plano de Continuidade

Este documento centraliza o estado atual, arquitetura, prioridades, roadmap, testes e evolução planejada do RenLocalizer.

O projeto possui atualmente uma CLI funcional para tradução de jogos Ren'Py. A evolução planejada mantém o Core em Python e adiciona uma aplicação desktop utilizando Electron + React + TypeScript.

---

# 1. Visão geral

O objetivo do RenLocalizer é fornecer uma ferramenta completa para tradução de jogos Ren'Py, inicialmente utilizando LibreTranslate, mas preparada para múltiplos providers e diferentes versões da engine.

A aplicação deverá possuir:

* Core de tradução em Python;
* CLI;
* Python Worker;
* aplicação desktop;
* React + TypeScript;
* Electron;
* sistema de cache;
* batching;
* retry e fallback;
* suporte a múltiplos providers;
* adapters para versões do Ren'Py;
* suporte progressivo a `.rpy`, `.rpyc`, `.rpa` e `.rpymc`;
* Deep Scan;
* Runtime Hook;
* relatórios;
* testes automatizados;
* distribuição para Windows e Linux.

Princípio principal:

> A interface pode mudar. O Core não deve precisar mudar para que outra interface seja criada.

---

# 2. Estado atual

## Funcionalidades já implementadas

* `ConfigManager` básico para carregar e salvar configurações.
* Fluxo principal parametrizado para:

  * caminho do projeto;
  * idioma;
  * cache.
* Remoção de caminhos hardcoded.
* Entrada legada delegando para o fluxo configurável.
* Implementações consolidadas em `core/`.
* Wrappers de compatibilidade mantidos quando necessários.
* Testes migrados para os módulos utilizados pela CLI.
* Validação de arquivos `.rpy` fonte fora de `game/tl/`.
* Parser de blocos `old/new`.
* Identificação de traduções pendentes.
* Detecção de menus nomeados.
* IDs compatíveis com Ren'Py.
* Suporte a menus.
* Suporte a `renpy.input()`.
* Suporte a screen strings.
* Suporte a escapes Ren'Py.
* CLI funcional.

---

# 3. Arquitetura geral

A arquitetura desejada é:

```
CLI
 │
 ▼
Python Core
 │
 ▼
TranslationPipeline
 │
 ├── Parser
 ├── Cache
 ├── Providers
 └── Engine Adapters
```

Para a aplicação desktop:

```
React
  │
  │ IPC
  ▼
Electron Main
  │
  │ stdio
  ▼
Python Worker
  │
  ▼
Python Core
```

A CLI e a GUI devem utilizar o mesmo Core.

---

# 4. Separação de responsabilidades

## 4.1 Python Core

O Core contém toda a lógica de negócio.

Responsabilidades:

* parsing;
* tradução;
* batching;
* cache;
* retry;
* fallback;
* providers;
* adapters;
* configuração;
* filesystem;
* geração dos arquivos;
* validação;
* compatibilidade Ren'Py.

O Core não deve conhecer:

* React;
* Electron;
* interface gráfica;
* terminal;
* shell específico;
* sistema operacional específico.

---

## 4.2 CLI

A CLI será uma interface para o Core.

Responsabilidades:

* argumentos;
* validação;
* logs;
* progresso;
* códigos de saída;
* execução do pipeline.

A CLI deve continuar existindo mesmo após a criação da GUI.

Ela será útil para:

* desenvolvimento;
* debugging;
* testes;
* automação;
* scripts;
* usuários avançados;
* processamento em lote.

---

## 4.3 Python Worker

O Worker será um processo separado responsável por conectar Electron ao Core.

Responsabilidades:

* receber comandos;
* executar operações;
* enviar progresso;
* enviar logs;
* enviar warnings;
* enviar erros;
* informar conclusão;
* permitir cancelamento;
* encerrar corretamente.

O Worker não deve duplicar lógica do Core.

---

## 4.4 Electron

Electron será responsável pela aplicação desktop.

Responsabilidades:

* criação da janela;
* processo principal;
* IPC;
* gerenciamento do Worker;
* seleção de arquivos;
* seleção de diretórios;
* integração com o sistema operacional;
* ciclo de vida da aplicação.

Electron será a ponte entre React e Python Worker.

---

## 4.5 React

React será responsável pela interface.

Responsabilidades:

* componentes;
* telas;
* formulários;
* estado;
* progresso;
* logs;
* configurações;
* interação com o usuário.

React não deve conter:

* parser Ren'Py;
* lógica de tradução;
* cache;
* batching;
* geração de `.rpy`;
* regras específicas do Ren'Py.

---

# 5. Estrutura planejada

```
RenLocalizer/
│
├── backend/
│   ├── core/
│   │   ├── parser/
│   │   ├── pipeline/
│   │   ├── translator/
│   │   ├── cache/
│   │   ├── providers/
│   │   ├── adapters/
│   │   ├── models/
│   │   └── config/
│   │
│   ├── worker/
│   │   ├── protocol/
│   │   ├── handlers/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── stores/
│   │   ├── types/
│   │   └── App.tsx
│   │
│   ├── electron/
│   │   ├── main.ts
│   │   └── preload.ts
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── cli/
├── data/
├── docs/
├── tests/
├── config.json
└── README.md
```

A estrutura poderá ser adaptada ao estado real do repositório.

O mais importante é manter a separação de responsabilidades.

---

# 6. Configuração

O projeto deverá possuir um `config.json` real.

Exemplo conceitual:

```
{
  "project": {
    "path": "",
    "language": "pt-br"
  },
  "translation": {
    "max_batch_size": 100,
    "max_retries": 3
  },
  "cache": {
    "enabled": true,
    "path": ""
  },
  "engine": {
    "provider": "libretranslate"
  }
}
```

O `ConfigManager` deverá permitir:

* valores padrão;
* configuração persistente;
* override por CLI;
* override pela GUI;
* validação;
* expansão futura.

---

# 7. Batching

O sistema deverá suportar tradução em lotes.

Requisitos:

* separar entradas encontradas no cache;
* identificar apenas entradas pendentes;
* proteger placeholders;
* proteger escapes Ren'Py;
* criar batches;
* utilizar `translation.max_batch_size`;
* iniciar com limite de até 100 entradas;
* enviar um lote por requisição quando o provider suportar;
* preservar a ordem;
* associar respostas aos respectivos `translation_id`;
* atualizar o cache após cada lote;
* respeitar `max_retries`;
* repetir lotes que falharem;
* dividir lotes problemáticos;
* tentar entradas individualmente como fallback;
* manter funcionamento com providers que não suportam listas.

O tamanho do batch não pode alterar a saída final.

---

# 8. Cache

Fluxo esperado:

```
Entrada
   │
   ▼
Existe no cache?
   │
   ├── Sim ──► Utilizar tradução
   │
   └── Não
         │
         ▼
       Batch
         │
         ▼
      Provider
         │
         ▼
       Cache
```

O cache deve ser atualizado após cada lote concluído.

Isso permite continuar o trabalho após:

* cancelamento;
* erro de provider;
* falha de rede;
* encerramento inesperado.

---

# 9. Retry e fallback

Fluxo:

```
Batch
  │
  ▼
Erro?
  │
  ├── Não ──► Continuar
  │
  └── Sim
        │
        ▼
      Retry
        │
        ▼
     Falhou?
        │
        ▼
   Dividir lote
        │
        ▼
 Tentar individualmente
```

O número máximo de tentativas deverá respeitar:

```
translation.max_retries
```

Entradas que continuarem falhando deverão ser registradas.

---

# 10. Parser de `tl/`

O parser de arquivos de tradução deverá ser integrado ao pipeline.

Objetivos:

* identificar blocos `old/new`;
* identificar traduções existentes;
* reutilizar traduções;
* detectar pendências;
* evitar traduções duplicadas;
* preservar estrutura;
* manter compatibilidade com o formato Ren'Py.

Exemplo:

```
game/
├── script.rpy
└── tl/
    └── pt-br/
        ├── dialogue.rpy
        └── strings.rpy
```

As traduções existentes deverão ser analisadas antes de enviar novas entradas ao provider.

---

# 11. Providers

O LibreTranslate deverá ser encapsulado em um provider.

Arquitetura:

```
TranslationProvider
├── LibreTranslateProvider
├── FutureProvider
└── FutureProvider
```

O pipeline deverá depender de uma interface abstrata e não diretamente do LibreTranslate.

Exemplo conceitual:

```
provider.translate(entries)
```

Isso permitirá adicionar novos providers sem alterar o pipeline principal.

---

# 12. Compatibilidade Ren'Py

A pipeline é específica para Ren'Py.

A versão atualmente utilizada como principal referência de validação é:

```
Ren'Py 8.5.2.26010301
```

Não declarar compatibilidade ampla sem testes.

A compatibilidade deverá ser isolada:

```
EngineAdapter
└── RenPyAdapter
    ├── RenPy7Profile
    └── RenPy8Profile
```

Os profiles poderão controlar:

* detecção da versão;
* IDs;
* hashes;
* encoding;
* normalização;
* menus nomeados;
* parsing;
* `.rpyc`;
* `.rpa`;
* `.rpymc`.

---

# 13. Detecção da versão

O sistema deverá tentar detectar automaticamente a versão do Ren'Py.

Caso a detecção não seja confiável, o usuário poderá escolher manualmente.

Exemplo:

```
Versão detectada:
[ Automático ▼ ]

Versão manual:
[ Ren'Py 8 ▼ ]
```

A versão utilizada deverá ser registrada no projeto e nos logs.

---

# 14. Ren'Py 7 e Ren'Py 8

Ren'Py 7 poderá funcionar parcialmente em scripts simples, mas não deve ser considerado certificado sem testes.

Processo:

1. detectar versão;
2. criar profile;
3. implementar regras específicas;
4. criar testes;
5. validar parsing;
6. validar IDs;
7. validar encoding;
8. validar arquivos compilados;
9. documentar limitações.

---

# 15. Arquivos suportados

Inicialmente:

```
.rpy
```

Posteriormente:

```
.rpyc
.rpa
.rpymc
```

Cada formato deverá possuir testes próprios.

O sistema não deverá tratar arquivos compilados ou empacotados como se fossem `.rpy` normais.

---

# 16. Deep Scan

O Deep Scan deverá realizar uma análise mais completa do projeto.

Objetivos:

* localizar `game/`;
* localizar `.rpy`;
* localizar `.rpyc`;
* localizar `.rpa`;
* localizar `.rpymc`;
* localizar `tl/`;
* identificar arquivos ignorados;
* detectar problemas;
* gerar diagnóstico.

Exemplo:

```
Project Scan

✓ game/
✓ 184 arquivos .rpy
✓ 23 arquivos .rpyc
✓ tl/ encontrado
⚠ 2 arquivos .rpa
⚠ versão Ren'Py não determinada
```

---

# 17. Runtime Hook

Funcionalidade futura.

Objetivos:

* identificar textos durante a execução;
* encontrar conteúdos não detectados pelo scan tradicional;
* auxiliar diagnóstico;
* complementar o pipeline.

O Runtime Hook não substituirá o processo normal de tradução.

---

# 18. Relatórios

O sistema deverá gerar relatórios contendo informações como:

* arquivos encontrados;
* arquivos processados;
* frases encontradas;
* traduções recuperadas do cache;
* novas traduções;
* erros;
* warnings;
* entradas ignoradas;
* batches executados;
* retries;
* entradas com falha;
* tempo de execução.

Exemplo:

```
RenLocalizer Report
────────────────────────────

Arquivos encontrados: 184
Arquivos processados: 181

Entradas:
  Total:       12.430
  Cache:        8.210
  Traduzidas:   4.180
  Falhas:          40

Batches:
  Executados:      42
  Retries:          3

Tempo:
  18m 32s
```

---

# 19. Python Worker

Estrutura:

```
backend/
└── worker/
    ├── protocol/
    ├── handlers/
    └── main.py
```

Fluxo:

```
Electron
   │
   │ spawn / stdio
   ▼
Python Worker
   │
   ▼
TranslationPipeline
```

O Worker deverá:

* iniciar;
* aguardar comandos;
* executar operações;
* emitir eventos;
* receber cancelamento;
* finalizar corretamente.

---

# 20. Protocolo do Worker

O protocolo deverá utilizar mensagens estruturadas.

## Comando de tradução

```
{
  "version": 1,
  "command": "translate",
  "project": "C:/Games/MyGame",
  "language": "pt-br"
}
```

## Progresso

```
{
  "version": 1,
  "event": "progress",
  "current": 150,
  "total": 500,
  "file": "script.rpy",
  "percentage": 30
}
```

## Log

```
{
  "version": 1,
  "event": "log",
  "level": "info",
  "message": "Lote 3 concluído"
}
```

## Warning

```
{
  "version": 1,
  "event": "warning",
  "message": "Provider não suportou batching"
}
```

## Erro

```
{
  "version": 1,
  "event": "error",
  "code": "TRANSLATION_FAILED",
  "message": "Falha ao acessar o provider"
}
```

## Conclusão

```
{
  "version": 1,
  "event": "completed",
  "translated": 500,
  "failed": 2
}
```

## Cancelamento

```
{
  "version": 1,
  "event": "cancelled",
  "message": "Tradução cancelada pelo usuário"
}
```

O protocolo deverá possuir:

* versão;
* comandos;
* eventos;
* tratamento de erros;
* progresso;
* logs;
* cancelamento;
* possibilidade de evolução futura.

---

# 21. Cancelamento

O usuário deverá conseguir cancelar uma tradução.

Fluxo:

```
React
  │
  │ cancel()
  ▼
Electron
  │
  ▼
Python Worker
  │
  ▼
TranslationPipeline
```

O pipeline deverá:

* impedir novas requisições;
* finalizar operações críticas;
* salvar o estado quando possível;
* preservar arquivos já concluídos;
* manter o cache consistente;
* registrar o cancelamento.

Evitar matar o processo abruptamente quando uma finalização controlada for possível.

---

# 22. React + TypeScript

A GUI será desenvolvida utilizando:

* React;
* TypeScript;
* Vite.

Estrutura:

```
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   ├── stores/
│   ├── types/
│   └── App.tsx
│
└── electron/
    ├── main.ts
    └── preload.ts
```

---

# 23. Telas iniciais

A primeira versão deverá possuir:

* Dashboard;
* Projeto;
* Tradução;
* Configurações;
* Logs.

## Dashboard

Mostrar:

* projeto atual;
* idioma;
* provider;
* versão Ren'Py;
* status;
* última tradução;
* estatísticas.

## Projeto

Permitir:

* selecionar pasta;
* validar projeto;
* detectar versão;
* executar scan.

## Tradução

Permitir:

* selecionar idioma;
* selecionar provider;
* iniciar;
* cancelar;
* acompanhar progresso.

## Configurações

Permitir configurar:

* provider;
* endpoint/API;
* cache;
* batch size;
* retries;
* idioma padrão;
* diretórios.

## Logs

Mostrar:

* informações;
* warnings;
* erros;
* progresso;
* operações.

---

# 24. Funcionalidades futuras da GUI

Posteriormente:

* gerenciamento de projetos;
* histórico de traduções;
* relatórios;
* configurações avançadas;
* gerenciamento de engines;
* diagnóstico;
* Deep Scan;
* Runtime Hook;
* validação de traduções;
* comparação de versões;
* estatísticas;
* gerenciamento do cache;
* reprocessamento seletivo;
* seleção de arquivos;
* filtros de tradução.

---

# 25. Electron

Electron será responsável por:

* janela;
* processo principal;
* IPC;
* preload;
* Worker;
* filesystem;
* process management;
* ciclo de vida.

Arquitetura:

```
React Renderer
      │
      │ IPC
      ▼
Electron Main
      │
      │ stdio
      ▼
Python Worker
```

---

# 26. Preload

O Renderer não deverá possuir acesso irrestrito ao Node.js.

O `preload.ts` deverá expor somente uma API controlada.

Exemplo:

```
window.renlocalizer
├── translate()
├── cancel()
├── selectDirectory()
├── selectFile()
├── getConfig()
├── saveConfig()
├── getProjectInfo()
└── onProgress()
```

Evitar:

```
React
  ↓
Node.js completo
```

Preferir:

```
React
  ↓
Preload API
  ↓
Electron Main
```

---

# 27. Segurança do Electron

O React não deverá acessar diretamente:

* Node.js;
* filesystem;
* `child_process`;
* shell;
* `process`.

Essas operações deverão permanecer nos processos apropriados.

O `preload` deverá expor somente métodos necessários.

---

# 28. Comunicação completa

## Início

```
Usuário
   ↓
React
   ↓
IPC
   ↓
Electron Main
   ↓
Python Worker
   ↓
TranslationPipeline
```

## Retorno

```
TranslationPipeline
   ↓
Python Worker
   ↓
Electron Main
   ↓
IPC
   ↓
React
   ↓
Interface
```

---

# 29. Interface não bloqueante

A tradução nunca deverá ser executada diretamente no Renderer.

O processamento deverá ocorrer no Python Worker.

Enquanto a tradução estiver sendo executada, a interface deverá continuar respondendo.

Eventos:

* `progress`;
* `log`;
* `warning`;
* `error`;
* `completed`;
* `cancelled`.

---

# 30. Portabilidade

Plataformas prioritárias:

* Windows;
* Linux.

Não utilizar:

* caminhos Windows hardcoded;
* comandos exclusivos de `cmd.exe`;
* comandos exclusivos de Bash;
* dependência de shell específico.

Python deverá utilizar `pathlib`.

Electron deverá utilizar APIs apropriadas do Node/Electron.

O Worker deverá possuir builds específicos por plataforma.

---

# 31. LibreTranslate

O LibreTranslate continuará sendo acessado via HTTP.

O endpoint deverá estar na configuração.

Exemplo:

```
{
  "provider": {
    "name": "libretranslate",
    "url": "http://localhost:5000"
  }
}
```

A aplicação não deverá depender de um caminho ou configuração específica do Windows.

---

# 32. Empacotamento

O usuário final não deverá precisar instalar manualmente:

* Python;
* Node.js;
* npm;
* dependências Python;
* dependências do projeto.

O pacote deverá conter:

* Electron;
* build React;
* Python Worker;
* dependências Python;
* assets;
* configuração inicial.

---

# 33. Windows

Objetivo:

```
RenLocalizer-Setup.exe
```

Tecnologia prevista:

* NSIS ou solução equivalente.

O instalador deverá incluir:

* Electron;
* React;
* Worker Python;
* dependências;
* assets;
* ícone;
* configuração inicial.

---

# 34. Linux

Formatos previstos:

* AppImage;
* `.deb`.

O AppImage poderá ser priorizado inicialmente.

---

# 35. Builds

Cada plataforma deverá possuir seu próprio build.

Windows:

```
Electron
   +
React build
   +
Python Worker Windows
```

Linux:

```
Electron
   +
React build
   +
Python Worker Linux
```

Não assumir que executáveis ou dependências de uma plataforma funcionarão diretamente em outra.

---

# 36. Testes

O projeto deverá utilizar múltiplas camadas de testes.

```
Unit Tests
    ↓
Core

Integration Tests
    ↓
Pipeline + Providers + Filesystem

Worker Tests
    ↓
Protocol + Commands + Events

Electron Tests
    ↓
IPC + Process Management

Frontend Tests
    ↓
React + State + Components

End-to-End
    ↓
React
  ↓
Electron
  ↓
Python
  ↓
TranslationPipeline
```

---

# 37. Testes do Core

Cobrir:

* parser;
* diálogos;
* menus;
* prompts;
* strings;
* escapes;
* placeholders;
* hashes;
* IDs;
* cache;
* batching;
* retry;
* fallback;
* providers;
* adapters;
* versões do Ren'Py;
* geração de arquivos.

---

# 38. Testes do Worker

Cobrir:

* comando válido;
* comando inválido;
* projeto inexistente;
* configuração inválida;
* início da tradução;
* progresso;
* logs;
* warnings;
* erros;
* conclusão;
* cancelamento;
* encerramento;
* Worker interrompido;
* mensagens inválidas.

---

# 39. Testes do Electron

Cobrir:

* inicialização;
* criação da janela;
* preload;
* IPC;
* inicialização do Worker;
* envio de comandos;
* recebimento de eventos;
* encerramento do Worker;
* falha do Worker;
* seleção de diretório;
* seleção de arquivos;
* comunicação com Renderer.

---

# 40. Testes do React

Cobrir:

* componentes;
* formulários;
* seleção de projeto;
* seleção de idioma;
* seleção de provider;
* estado da tradução;
* barra de progresso;
* logs;
* warnings;
* erros;
* cancelamento;
* conclusão.

---

# 41. Testes End-to-End

O fluxo completo deverá ser validado:

```
Usuário
   ↓
React
   ↓
Electron
   ↓
Python Worker
   ↓
TranslationPipeline
   ↓
Parser
   ↓
Cache
   ↓
Provider
   ↓
Arquivos traduzidos
```

Casos importantes:

* projeto válido;
* projeto inexistente;
* pasta `game/` inexistente;
* `.rpy` inválido;
* cache existente;
* cache parcial;
* erro em batch;
* retry;
* fallback individual;
* provider indisponível;
* cancelamento;
* erro do Worker;
* encerramento inesperado;
* caminhos com espaços;
* caminhos Unicode;
* Windows;
* Linux.

---

# 42. Ordem de implementação do Core

A ordem recomendada é:

1. Batching.
2. Cache + Retry + Fallback.
3. Parser de `tl/`.
4. Providers / engine selecionável.
5. EngineAdapter.
6. Detecção de versão Ren'Py.
7. Profiles Ren'Py 7/8.
8. Suporte a `.rpyc`.
9. Suporte a `.rpa`.
10. Suporte a `.rpymc`.
11. Deep Scan.
12. Runtime Hook.
13. Relatórios.

---

# 43. Ordem de implementação da GUI

A GUI deverá ser implementada nesta ordem:

1. Definir protocolo do Worker.
2. Implementar Python Worker.
3. Testar Worker sem GUI.
4. Criar projeto Electron.
5. Configurar Electron Main.
6. Criar `preload.ts`.
7. Implementar IPC.
8. Criar React + TypeScript + Vite.
9. Criar tela principal.
10. Seleção do projeto.
11. Configuração de idioma.
12. Configuração de engine/provider.
13. Iniciar tradução.
14. Progresso em tempo real.
15. Logs.
16. Cancelamento.
17. Tratamento de erros.
18. Testes de integração.
19. Testes E2E.

---

# 44. Ordem geral do projeto

A evolução completa deverá seguir aproximadamente:

```
1. Core
   ↓
2. Batching
   ↓
3. Cache / Retry / Fallback
   ↓
4. Parser tl/
   ↓
5. Providers
   ↓
6. Compatibilidade Ren'Py
   ↓
7. Arquivos compilados/empacotados
   ↓
8. Deep Scan / Runtime Hook / Relatórios
   ↓
9. CLI
   ↓
10. Worker
   ↓
11. Electron
   ↓
12. React
   ↓
13. Integração
   ↓
14. Testes E2E
   ↓
15. Empacotamento
   ↓
16. Distribuição
```

Essa ordem evita criar uma interface sobre um Core instável.

---

# 45. Prioridade atual

A prioridade imediata é:

```
1. Batching
2. Cache + Retry + Fallback
3. Parser de tl/
4. Providers / Engine selecionável
5. Compatibilidade Ren'Py
6. .rpyc / .rpa / .rpymc
7. Deep Scan / Runtime Hook / Relatórios
8. Estabilização da CLI
9. Contrato do Worker
10. Python Worker
11. Electron
12. React + TypeScript
13. Integração
14. Testes E2E
15. Empacotamento
```

A GUI poderá começar antes de todas as funcionalidades futuras do Core estarem prontas, desde que o contrato do Worker esteja definido.

---

# 46. Princípios arquiteturais

## Core independente

O Core não conhece a interface.

## CLI independente

A CLI utiliza o Core diretamente.

## Worker independente

O Worker utiliza o Core e pode ser executado sem GUI.

## Electron como ponte

Electron conecta a interface ao Worker.

## React como apresentação

React controla a experiência visual.

## Comunicação baseada em eventos

Operações longas devem emitir eventos.

## Provider independente

O Core não depende diretamente do LibreTranslate.

## Compatibilidade isolada

Regras específicas de versões do Ren'Py ficam nos adapters/profiles.

## Portabilidade

Nenhuma camada deve depender de um sistema operacional específico.

## Baixo acoplamento

Cada camada conhece somente aquilo que precisa.

## Contratos explícitos

A comunicação entre camadas deve possuir interfaces e protocolos claros.

## Testabilidade

Cada camada deve poder ser testada isoladamente.

## Compatibilidade retroativa

A CLI existente deve continuar funcionando durante a evolução para a GUI.

---

# 47. Arquitetura final

```
                        RenLocalizer
                          │
           ┌──────────────┴──────────────┐
           │                             │
          CLI                           GUI
           │                             │
           │                    React + TypeScript
           │                             │
           │                          Electron
           │                             │
           │                            IPC
           │                             │
           └──────────────┬──────────────┘
                          │
                          ▼
                   Python Worker
                          │
                          ▼
                TranslationPipeline
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
      Parser            Cache          Providers
         │                                 │
         ▼                                 ▼
    Ren'Py Files                    Translation APIs
         │
         ▼
  Engine Adapters
         │
   ┌─────┴─────┐
   ▼           ▼
Ren'Py 7    Ren'Py 8
```

---

# 48. Regra central do projeto

O RenLocalizer deverá ser desenvolvido de forma que:

```
CLI ─────────┐
             │
GUI ─────────┼──► Python Core
             │
Worker ──────┘
```

A GUI é apenas uma nova forma de utilizar o sistema.

A lógica de tradução permanece no Python Core.

A CLI não será descartada após a criação da GUI.

O Electron não conterá a lógica de tradução.

O React não conterá a lógica de tradução.

O Python Worker não duplicará o Core.

Cada camada possuirá uma responsabilidade clara.

---

# 49. Resultado esperado

Ao final, o RenLocalizer deverá possuir:

```
┌──────────────────────────────────────────────┐
│                  RenLocalizer                │
├──────────────────────────────────────────────┤
│                                              │
│  CLI                                         │
│  └── Automação / Terminal / Desenvolvimento  │
│                                              │
│  Desktop App                                 │
│  ├── React + TypeScript                      │
│  ├── Electron                                │
│  └── Python Worker                           │
│                                              │
│  Python Core                                 │
│  ├── Parser                                  │
│  ├── TranslationPipeline                     │
│  ├── Batching                                │
│  ├── Cache                                   │
│  ├── Retry / Fallback                        │
│  ├── Providers                               │
│  ├── EngineAdapters                          │
│  ├── Compatibilidade Ren'Py                  │
│  ├── Deep Scan                               │
│  ├── Runtime Hook                            │
│  └── Relatórios                              │
│                                              │
│  Distribuição                                │
│  ├── Windows                                 │
│  └── Linux                                   │
│                                              │
└──────────────────────────────────────────────┘
```

---

# 50. Objetivo arquitetural final

O RenLocalizer deverá possuir um núcleo Python sólido, independente e testável.

A partir desse núcleo poderão existir múltiplas interfaces:

```
Python Core
   │
   ├── CLI
   │
   └── Python Worker
          │
          └── Electron
                │
                └── React
```

Dessa forma:

* a CLI continua funcionando;
* a GUI pode evoluir independentemente;
* o Core permanece reutilizável;
* novos providers podem ser adicionados;
* novas versões do Ren'Py podem ser suportadas;
* novos formatos podem ser implementados;
* Windows e Linux podem ser suportados;
* os componentes podem ser testados separadamente;
* a aplicação pode ser distribuída como desktop app.

> **Regra definitiva: a interface pode mudar; o Core permanece como o núcleo do RenLocalizer.**
