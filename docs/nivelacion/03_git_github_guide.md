# Nivelación: Git y GitHub para el Diplomado

> **¿Para quién?** Si usas Git solo con `git add . && git commit -m "fix" && git push` y
> nunca has abierto un Pull Request desde la línea de comandos, o si no sabes qué
> hace `git rebase` ni por qué importa el historial. Tiempo estimado: 1.5-2 horas.
>
> En el diplomado el historial de commits ES parte de la evaluación.
> Un repo con mensajes tipo "asdfgh" o "fix final final v3" comunica lo contrario
> de lo que buscas en una defensa técnica.

---

## 1. El modelo mental correcto

Git no es un sistema de backup. Es un **grafo de snapshots** con autoría y mensajes.
GitHub no es "donde guardas el código". Es la plataforma donde el instructor
revisa tu trabajo, el CI corre, y el historial queda público para reclutadores.

```
Tu máquina                     GitHub (remoto)
─────────────────────────────  ────────────────────────────
Working directory              origin/main
    ↓ git add                       ↑
Staging area                   origin/feature/m1-harness
    ↓ git commit
Local main ──── git push ──────────→
Local feature/m1-harness ──────────→
```

---

## 2. Configuración inicial (una sola vez)

```bash
# Identidad — aparece en cada commit
git config --global user.name  "Tu Nombre"
git config --global user.email "tu@email.com"

# Editor por defecto (VS Code es más cómodo que vim)
git config --global core.editor "code --wait"

# Rama principal se llama 'main', no 'master'
git config --global init.defaultBranch main

# Verificar configuración
git config --global --list
```

---

## 3. Flujo de trabajo en el diplomado

### Setup inicial (solo una vez, al aceptar el assignment)

```bash
# 1. Clona TU repo (el que GitHub Classroom creó para ti)
#    Classroom: https://classroom.github.com/classrooms/254552850-ia-aplicada-al-desarrollo-de-software
git clone https://github.com/ia-aplicada-al-desarrollo-de-software/[tu-repo-asignado].git
cd [tu-repo-asignado]

# 2. Verifica que apunta al origen correcto
git remote -v
# Debe mostrar:
# origin  https://github.com/ia-aplicada-al-desarrollo-de-software/[tu-repo].git

# 3. Setup del ambiente
uv sync --all-groups
```

### Ciclo por módulo (se repite cada entrega)

```bash
# 1. Asegúrate de estar en main actualizado
git checkout main
git pull origin main

# 2. Crea la rama del módulo
git checkout -b feature/m1-harness
# Nombre de rama: feature/m1-harness, feature/m2-arquitectura, etc.

# 3. Trabaja: edita archivos, escribe tests
# (Ciclo: edit → test local → commit)

# 4. Commits atómicos — un commit = un cambio lógico
git add app/main.py tests/test_sanity.py
git commit -m "feat(m1): add /spec endpoint with Pydantic schema"

# 5. Verifica el harness ANTES de pushear
uv run --frozen ruff check . && uv run --frozen mypy app/ --ignore-missing-imports && uv run --frozen pytest -q

# 6. Pushea la rama
git push origin feature/m1-harness

# 7. Abre el Pull Request en GitHub (o desde CLI con gh)
gh pr create --base main --head feature/m1-harness \
  --title "M1: Harness Engineering" \
  --body "Agrega mypy + bandit al CI. Primer endpoint documentado. CI verde."
```

---

## 4. Mensajes de commit — el estándar del diplomado

El formato **Conventional Commits** es el estándar del mercado 2026 y lo que
el instructor espera ver en tu historial:

```
<tipo>(<alcance>): <descripción corta en imperativo>

[cuerpo opcional — explica el POR QUÉ, no el QUÉ]

[footer opcional — referencias a issues, breaking changes]
```

| Tipo | Cuándo usarlo |
|------|--------------|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `test` | Agregar o corregir tests |
| `docs` | Solo documentación |
| `refactor` | Cambio de código sin cambiar comportamiento |
| `ci` | Cambios en el pipeline de CI |
| `chore` | Tareas de mantenimiento (deps, config) |

**Ejemplos concretos del diplomado:**

```bash
# Bien ✅
git commit -m "feat(agent): implement ReAct loop with MAX_STEPS guard"
git commit -m "test(m3): add TDD tests for AlertService threshold logic"
git commit -m "fix(pydantic): use Decimal instead of float for PCI compliance"
git commit -m "ci: add mypy and bandit steps to workflow"
git commit -m "docs: complete README with docker-compose instructions"

# Mal ❌ — el evaluador ve esto en el historial de tu defensa
git commit -m "fix"
git commit -m "arreglé cosas"
git commit -m "funcionó!!!"
git commit -m "commit final v2 este si"
git commit -m "wip"
```

**Regla:** Si no puedes describir el commit en una línea clara, probablemente
está haciendo demasiadas cosas. Divide el trabajo en commits más pequeños.

---

## 5. Cómo funciona el Pull Request

Un PR en este diplomado no es un formalismo. Es el artefacto de evaluación:
el instructor ve tu diff, los comentarios del CI, y puede hacer code review.

```
feature/m1-harness ──→ [PR] ──→ main
                         │
                         ├── CI corre automáticamente
                         ├── Si CI falla: PR bloqueado (no puedes mergear)
                         ├── Instructor hace code review
                         └── Si todo verde: mergeas
```

### Anatomy de un buen PR

**Título:** `M1: Harness Engineering — ruff + mypy + bandit + /spec endpoint`

**Descripción (en el body del PR):**
```markdown
## Qué hace este PR
- Agrega mypy y bandit al CI (después de ruff)
- Implementa endpoint GET /spec que retorna el contrato de la API
- Agrega test de esquema Pydantic para SpecResponse

## Decisiones de diseño
- Usé Literal["ok"] en SpecResponse.status para tipado estricto (no solo str)
- El CI corre mypy solo sobre app/ (no agent/ — todavía vacío en M1)

## Testing
- CI verde: https://github.com/[org]/[repo]/actions/runs/[id]
- Cobertura: 72%

## AI Usage
Ver AI_USAGE.md — usé Claude Code para generar el skeleton del test de esquema,
modifiqué el assert de version_format.
```

---

## 6. Comandos que usarás más seguido

```bash
# Estado actual del repo
git status
git diff                    # Cambios no staged
git diff --staged           # Cambios staged (listos para commit)

# Historial
git log --oneline -10       # Últimos 10 commits en una línea
git log --oneline --graph   # Historial como árbol (útil con ramas)

# Ramas
git branch                  # Lista ramas locales
git branch -a               # Lista ramas locales Y remotas
git checkout -b nueva-rama  # Crear y cambiar a nueva rama
git checkout main           # Volver a main

# Sincronización
git fetch origin            # Descarga cambios remotos (sin aplicarlos)
git pull origin main        # fetch + merge
git push origin feature/x   # Sube la rama feature/x al remoto

# Deshacer (con cuidado)
git restore app/main.py     # Descarta cambios en un archivo (irreversible)
git reset HEAD app/main.py  # Unstage un archivo (no pierde cambios)
git stash                   # Guarda cambios temporalmente sin commitear
git stash pop               # Recupera los cambios guardados

# Ver diferencias entre ramas
git diff main..feature/m1-harness
```

---

## 7. El CI de GitHub Actions

Cada push a cualquier rama dispara el pipeline en `.github/workflows/ci.yml`.
Puedes ver el resultado en la pestaña **Actions** de tu repo en GitHub.

```
Push a feature/m1-harness
        ↓
GitHub Actions inicia el job "test"
        ↓
  ├── Checkout del código
  ├── Setup Python 3.12
  ├── Install uv + sync deps
  ├── ruff check .         → ❌ si hay errores de estilo
  ├── mypy app/            → ❌ si hay errores de tipo
  ├── bandit -r app/       → ❌ si hay vulnerabilidades
  └── pytest --cov=app     → ❌ si tests fallan o cobertura < 60%
        ↓
CI verde ✅ → PR se puede mergear
CI rojo  ❌ → PR bloqueado hasta que lo corrijas
```

**Cómo leer un error de CI:**
1. Click en la pestaña **Actions** en GitHub
2. Click en el run fallido (ícono rojo)
3. Click en el step que falló (ej: "Type check (mypy)")
4. Lee el output — la línea del error dice exactamente qué archivo y qué línea

---

## 8. Errores comunes y soluciones

**Error: `push rejected — branch protection rule`**
```bash
# No puedes pushear directo a main. Es correcto — usa una rama y PR.
git checkout -b feature/fix-typo
git push origin feature/fix-typo
# Luego abre el PR desde GitHub
```

**Error: `merge conflict` al hacer pull**
```bash
git pull origin main
# Auto-merging app/main.py
# CONFLICT (content): Merge conflict in app/main.py

# 1. Abre el archivo — verás marcadores <<<<<<< ======= >>>>>>>
# 2. Edita manualmente para quedarte con la versión correcta
# 3. git add app/main.py
# 4. git commit -m "fix: resolve merge conflict in main.py"
```

**Error: `your branch is behind origin/main`**
```bash
git checkout main
git pull origin main
git checkout feature/mi-rama
git rebase main  # Mueve tus commits encima del main actualizado
```

**Error: commiteé el .env con la API key**
```bash
# URGENTE — hazlo inmediatamente, la key puede haber quedado en GitHub
# 1. Revoca la API key en el panel del proveedor (OpenAI, Anthropic)
# 2. Elimina el archivo del historial:
git filter-repo --path .env --invert-paths
# 3. Force push (necesita permiso del instructor si branch protection está activo)
git push origin main --force-with-lease
# 4. Verifica que .env está en .gitignore
```

---

## 9. GitHub CLI (gh) — opcional pero muy útil

```bash
# Instalar: https://cli.github.com/
brew install gh         # Mac
winget install GitHub.cli  # Windows

# Autenticar
gh auth login

# Crear PR desde terminal (sin abrir el browser)
gh pr create --base main --head feature/m1-harness \
  --title "M1: Harness Engineering" \
  --body "CI verde con ruff+mypy+bandit. Cobertura 72%."

# Ver status del CI del último PR
gh pr checks

# Ver lista de PRs abiertos
gh pr list

# Mergear cuando CI está verde
gh pr merge --squash
```

---

## Recursos

- [Git — libro oficial (español)](https://git-scm.com/book/es/v2)
- [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/)
- [GitHub CLI docs](https://cli.github.com/manual/)
- [GitHub Actions — Understanding workflows](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions)
