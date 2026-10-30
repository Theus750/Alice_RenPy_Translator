---
name: RenLocalizer Design System
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#c2c6d6'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#8c909f'
  outline-variant: '#424754'
  surface-tint: '#adc6ff'
  primary: '#adc6ff'
  on-primary: '#002e6a'
  primary-container: '#4d8eff'
  on-primary-container: '#00285d'
  inverse-primary: '#005ac2'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#ffb95f'
  on-tertiary: '#472a00'
  tertiary-container: '#ca8100'
  on-tertiary-container: '#3e2400'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
  slate-surface: '#1E293B'
  slate-surface-elevated: '#273549'
  slate-border: '#334155'
  slate-border-subtle: '#1E293B'
  error-red: '#EF4444'
  error-red-bg: '#451A1A'
  warning-amber-bg: '#422006'
  success-emerald-bg: '#064E3B'
  info-blue-bg: '#172554'
  tag-renpy-token: '#818CF8'
  tag-renpy-token-bg: '#1E1B4B'
  text-primary: '#F8FAFC'
  text-secondary: '#94A3B8'
  text-muted: '#64748B'
  text-code: '#E2E8F0'
typography:
  display:
    fontFamily: Inter
    fontSize: 1.75rem
    fontWeight: '600'
    lineHeight: 2.25rem
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 1.25rem
    fontWeight: '600'
    lineHeight: 1.75rem
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: '600'
    lineHeight: 1.5rem
    letterSpacing: -0.01em
  body-base:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: 1.375rem
  body-dense:
    fontFamily: Inter
    fontSize: 0.8125rem
    fontWeight: '400'
    lineHeight: 1.25rem
  label-code:
    fontFamily: JetBrains Mono
    fontSize: 0.8125rem
    fontWeight: '500'
    lineHeight: 1.25rem
  label-token:
    fontFamily: JetBrains Mono
    fontSize: 0.75rem
    fontWeight: '500'
    lineHeight: 1rem
  caption-mono:
    fontFamily: JetBrains Mono
    fontSize: 0.6875rem
    fontWeight: '400'
    lineHeight: 1rem
  metric-val:
    fontFamily: JetBrains Mono
    fontSize: 1.5rem
    fontWeight: '700'
    lineHeight: 1.875rem
    letterSpacing: -0.03em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  px: 1px
  0-5: 0.125rem
  '1': 0.25rem
  1-5: 0.375rem
  '2': 0.5rem
  '3': 0.75rem
  '4': 1rem
  '5': 1.25rem
  '6': 1.5rem
  '8': 2rem
  '10': 2.5rem
  rail-width: 15rem
  status-bar-height: 1.75rem
  table-row-height: 2.25rem
  header-height: 3.25rem
---

## Brand & Style

The design system establishes a high-performance, developer-grade desktop utility tailored specifically for script translation, syntax sanitization, and localized asset packaging for Ren'Py visual novels. Drawing inspiration from modern technical IDEs (e.g., VS Code, Linear, Crowdin, Poedit), the visual atmosphere prioritizes operational clarity, information density, and fatigue-free inspection over decorative flair.

### Visual Aesthetic: High-Density Technical Precision
The design language adopts a dark-first, crisp mechanical layout characterized by:
- **Zero-clutter structural containment**: High-contrast slate backgrounds paired with low-contrast structural dividers ensure deep focus during long bilingual review sessions.
- **Syntax & Placeholder Awareness**: Distinct visual treatment for inline placeholders (`[player]`, `{color=#fff}`), Ren'Py escape tags, and interpolation brackets to guarantee translation safety.
- **Deterministic State Modeling**: Immediate, unambiguous signal color coding (validation pass, warning flag, parser fault, worker active).
- **Desktop Density**: Tight spatial cadence, compact metric cards, and responsive bilingual data grids engineered to display thousands of entries without cognitive overload.

## Colors

The palette is tuned specifically for long working hours in front of technical text, utilizing an institutional deep-slate baseline with targeted chromatic indicators:

- **Primary (`#3B82F6`)**: Applied to primary CTA buttons ("Iniciar tradução", "Testar conexão"), active navigational rail states, active tab highlights, and focused interactive controls.
- **Secondary / Success (`#10B981`)**: Dedicated to positive pipeline checkpoints, valid folder confirmations (`game/` detected), 100% completed progress bars, and validated glossary matches.
- **Tertiary / Warning (`#F59E0B`)**: Signals pending human reviews, altered variables/placeholders, warning logs, and non-fatal engine disconnect alerts.
- **Error (`#EF4444`)**: Dictated for missing `game/` roots, HTTP/RPC worker dropouts (LibreTranslate connection failure), malformed `.rpy` scripts, and corrupted placeholders.
- **Token Color (`#818CF8`)**: Distinct lavender-blue accent isolated for engine tokens, Ren'Py string interpolations (`[player]`, `{i}`), and regex matches.

### Accessibility & Balance
Dark mode functions as the primary visual mode. In light mode environments, the background shifts to a calm `#F8FAFC`, with `#FFFFFF` cards, `#CBD5E1` borders, and intensified text tokens (`#0F172A`) ensuring WCAG AAA compliant text contrast throughout.

## Typography

The type system blends the neutral readability of **Inter** for core UI interactions and long-form conversational text, with the structured clarity of **JetBrains Mono** for script tokens, Ren'Py interpolation syntax, file paths, line pointers, and log streams.

- **Proportional Core**: Inter handles section headers, settings forms, button text, and translated dialogue. Its wide aperture and neutral geometric tone maximize reading throughput during intensive multi-hour proofreading.
- **Monospace Workhorse**: JetBrains Mono serves in translation grid columns where text integrity and syntax symbols are scrutinized. It eliminates ambiguity between characters like `0` / `O` and `1` / `l`, essential for variable anchors like `{size=+2}`, `[player_name]`, and indentation checks in `.rpy`.

## Layout & Spacing

The application architecture utilizes an uncompromising fixed-structural frame optimized for desktop screens (standard minimum 1280x800, target 1920x1080), avoiding fluid white-space vacuums in favor of predictable tool ergonomics.

### Layout Topology
1. **Global App Frame**:
   - **Header Bar (3.25rem / 52px)**: Houses project switcher, active engine badge (`LibreTranslate`), window management, and global config launcher.
   - **Persistent Sidebar Navigation (15rem / 240px)**: Anchored to the left with strict category grouping, count pills, and engine heartbeat indicators.
   - **Workbench Workspace (Flex 1)**: Divided either as split review grids (master-detail), stacked pipeline workflows, or full-width analytical metric decks.
   - **Operational Status Bar (1.75rem / 28px)**: Bottom-docked terminal-like ribbon reporting instantaneous engine state, queue counts, and memory/cache utilization.
2. **Spacing Grid**:
   - Built around an intentional **4px / 8px scale**.
   - Input controls, chips, and table cells utilize compact vertical padding (`0.375rem` / `0.5rem`) to maximize the visible string count per viewport screen without inducing visual clipping.

## Elevation & Depth

This design system avoids theatrical, floating dropped shadows. Visual hierarchy is established via **tonal layering (stacking surfaces)** and **precise 1px ghost borders**:

- **Base Layer (`#0F172A`)**: The desktop application viewport canvas.
- **Surface Container Tier 1 (`#1E293B`)**: Standard cards, table backgrounds, and main sidebar background, bordered by `1px solid #334155`.
- **Surface Container Tier 2 (`#273549`)**: Active input fields, hovered table rows, selected file list rows, and sticky table header strips.
- **Surface Container Tier 3 / Flyouts (`#334155`)**: Context menus, tooltips, and modal diagnostic windows with a razor-thin top highlight `border-t: 1px solid rgba(255, 255, 255, 0.1)`.
- **Shadow Signature**: When overlays or popovers appear, depth is rendered strictly using an ambient dark silhouette: `box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.45)`.

## Shapes

The design system uses a crisp, utilitarian **Level 1 (Soft)** shape geometry:
- **Base radius (`0.25rem` / 4px)**: Default for input fields, buttons, progress track bounds, table selection highlights, and badge tags.
- **Container radius (`0.5rem` / 8px)**: Applied to high-level metric cards, modal dialog shells, and collapsible log viewport panels.
- **Tab / Pill radius (`0.25rem` / 4px)**: Segmented switchers maintain low radius to reinforce an authentic engineering/IDE paradigm over consumer-app bubbly forms.
- **Variables / Token tags (`0.125rem` / 2px)**: Micro-radius for inline Ren'Py tags (`[player]`, `{b}`) to visually simulate terminal tokens.

## Components

### 1. Navigation Rail
- Fixed vertical rail containing items: Visão Geral, Projeto, Tradução, Revisão, Arquivos Gerados, Glossário, Configurações.
- Selected items feature a left vertical indicator (`3px solid #3B82F6`), surface tint (`#273549`), and contrast label (`#F8FAFC`). Unselected items rest at `#94A3B8`.

### 2. Buttons
- **Primary**: Background `#2563EB`, text `#FFFFFF`, hover `#1D4ED8`, active `#1E40AF`. Compact padding `0.375rem 0.875rem`, font-weight 500.
- **Secondary / Ghost**: Transparent background, border `1px solid #334155`, text `#94A3B8`, hover border `#475569`, hover text `#F8FAFC`.
- **Danger**: Border or background utilizing `#EF4444` for irreversible actions (e.g., reset cache, overwrite translation files).

### 3. Metric Summary Cards
- Compact stats blocks containing:
  - Uppercase micro-label (`caption-mono`, `#64748B`).
  - Hero figure (`metric-val`, `#F8FAFC`).
  - Subtext indicator (`body-dense`, emerald for cached hits, amber for pending items).
- Subtle background `#1E293B`, border `1px solid #334155`.

### 4. Bilingual Translation Data Grid
- **Header**: Sticky `#1E293B` bar with 1px bottom border `#334155`. Columns for: Type, Original String, Target String, Status.
- **Rows**: Alternating subtle backgrounds (`#0F172A` / `#141E33`). Height set to `2.25rem` (36px). Hover state `#1E293B`.
- **Inline Variable Tokens**: Strings with bracketed tags like `[player]` or `{i}` render these segments wrapped in a pill badge (`bg: #1E1B4B`, `color: #818CF8`, `border: 1px solid #3730A3`, font: `label-token`). Missing placeholders trigger an amber or red warning outline.

### 5. Multi-Stage Pipeline Progress
- Composed of a split vertical sequence showing verification checklist steps alongside a unified progress track.
- Filled portion is solid `#3B82F6` (transitions to `#10B981` on 100% completion).
- Stage status badges:
  - Completed: Green checkmark icon with `#10B981`.
  - In Progress: Pulsing blue dot with `#3B82F6` and real-time count `804 / 1284`.
  - Blocked/Queued: Text `#64748B`.

### 6. Collapsible Log & Diagnostics Console
- Dedicated expandable tray docked at bottom or side.
- Background `#090D16`, text `#94A3B8`, font `JetBrains Mono`.
- Timestamps highlighted in `#64748B`, info logs `#3B82F6`, warnings `#F59E0B`, errors `#EF4444`. Includes quick-action button to copy raw output or filter by stack trace.