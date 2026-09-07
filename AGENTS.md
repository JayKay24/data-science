# AGENTS.md - Monorepo Engineering Instructions & Standards

This document establishes mandatory guidelines, workflows, and conventions for AI coding agents operating within this data science monorepo. Agents MUST adhere strictly to these rules.

---

## 1. Core Architecture & Philosophy

- **Pants Build System**: We use Pants (`./pants`) for fine-grained dependency tracking, target-level caching, test isolation, and artifact packaging.
- **Shared Libraries (`libs/`)**: Common utility code, custom evaluation metrics, preprocessing routines, and schemas live under `libs/<lib_name>`. Shared libraries MUST be parametrized across all downstream project resolves that consume them.
- **Isolated Projects (`projects/`)**: Each portfolio data science project lives in its own directory under `projects/<project_name>`.
- **Multi-Resolve Isolation**: Projects MUST use dedicated resolves and lockfiles (`3rdparty/python/<project_name>.lock`). NEVER bundle conflicting machine learning frameworks into a single monolithic lockfile.

---

## 2. The #1 Pants Rule: Target Addresses, NEVER File Paths

### Strict Rule
Agents **MUST ALWAYS** use target addresses when invoking Pants commands. Agents **MUST NEVER** pass raw file paths to `./pants test`, `./pants check`, or `./pants package`.

### Why This Is Mandatory
Target addresses and file paths produce completely different Pants cache keys. Passing raw file paths breaks memoization, fragments the cache, and causes unnecessary cache misses.

```bash
# ✅ CORRECT (Uses target address cache):
./pants test projects/churn_prediction:tests
./pants test libs/core:tests
./pants test ::

# ❌ WRONG (Fragments cache and loses memoization):
./pants test projects/churn_prediction/churn_prediction/tests/test_api.py
```

---

## 3. Dependency Management Protocol (Multi-Resolve)

Every project and shared library is assigned a named resolve in `pants.toml`. When dependencies change:

1. **Update Requirements**:
   - Edit the appropriate file in `3rdparty/python/<name>-requirements.txt`.
   - Ensure the requirement target is declared in `3rdparty/python/BUILD` using `python_requirements(..., resolve="<resolve_name>")`.
2. **Register in `pants.toml`**:
   - Ensure the resolve mapping exists under `[python.resolves]` and `[python.resolves_to_interpreter_constraints]`.
3. **Regenerate Lockfiles**:
   - Run the generator for the specific resolve (or all resolves):
     ```bash
     ./pants generate-lockfiles --resolve=<resolve_name>
     # Or update all:
     ./pants generate-lockfiles
     ```
4. **Link Shared Libraries**:
   - If a project imports from `libs/core`, ensure `libs/core/BUILD` contains:
     ```python
     python_sources(
         name="core_lib",
         sources=["core/**/*.py"],
         resolve=parametrize("core_resolve", "<project_resolve>", ...),
     )
     ```
   - In the downstream project's `BUILD`:
     ```python
     python_sources(
         name="sources",
         sources=["<project_name>/**/*.py"],
         resolve="<project_resolve>",
         dependencies=[
             "libs/core:core_lib@resolve=<project_resolve>",
         ],
     )
     ```

---

## 4. Data Science & Machine Learning Engineering Standards

1. **Determinism & Reproducibility**:
   - All models, random splits, data samplers, and simulations **MUST** explicitly specify a random seed (e.g., `seed=42` or `np.random.seed(42)`).
2. **Decoupled Architecture**:
   - **Data Preprocessing & Features**: Pure, side-effect-free functions transforming DataFrames/arrays.
   - **Training Pipelines**: Standalone scripts/modules with a clean entrypoint function.
   - **Inference & Serving**: Decoupled from training code (e.g., FastAPI endpoints that load serialized artifacts or models).
3. **Type Annotations**:
   - All Python code **MUST** include complete type annotations (parameters and return types) to satisfy Mypy (`check_untyped_defs = True`).
   - If third-party packages lack types, leverage typed interfaces or configure `mypy.ini` appropriately without disabling global type safety.
4. **Notebook Hygiene (`.ipynb`)**:
   - Notebooks in `projects/<project_name>/notebooks/` are for exploratory analysis and presentation.
   - Core algorithms, preprocessing logic, and model training **MUST NOT** reside solely in notebooks; extract reusable logic into project Python modules.
5. **Path Portability**:
   - **NEVER** use absolute filesystem paths. Use relative paths resolved against `pathlib.Path(__file__).parent` or data loader parameters.

---

## 5. Step-by-Step Recipe: Adding a New Project

When instructed to create a new project (e.g., `projects/fraud_detection`), agents **MUST** execute the following sequence:

1. **Create Directory Structure**:
   ```bash
   mkdir -p projects/<project_name>/<project_name>/tests projects/<project_name>/notebooks
   ```
2. **Add Source Root**:
   - Add `"/projects/<project_name>"` to `root_patterns` under `[source]` in `pants.toml`.
3. **Define Dependencies & Resolve**:
   - Create `3rdparty/python/<project_name>-requirements.txt`.
   - Add resolve to `pants.toml`:
     ```toml
     [python.resolves]
     <project_name>_resolve = "3rdparty/python/<project_name>.lock"

     [python.resolves_to_interpreter_constraints]
     <project_name>_resolve = ["==3.11.*"]
     ```
   - Add `python_requirements` to `3rdparty/python/BUILD`:
     ```python
     python_requirements(
         name="<project_name>_reqs",
         source="<project_name>-requirements.txt",
         resolve="<project_name>_resolve",
     )
     ```
   - Parametrize `libs/core/BUILD` to include `<project_name>_resolve`.
4. **Create `projects/<project_name>/BUILD`**:
   - Define `python_sources`, `python_tests`, and executable/container targets (`pex_binary`, `docker_image`).
5. **Generate Lockfile**:
   ```bash
   ./pants generate-lockfiles --resolve=<project_name>_resolve
   ```
6. **Implement Code & Tests**:
   - Write source modules with type hints.
   - Write comprehensive unit tests in `<project_name>/tests/`.
7. **Run Mandatory Verification Gate** (see Section 6).

---

## 6. Mandatory Quality Gate & Verification Checklist

Before completing any code modifications, additions, or refactors, agents **MUST** run the full quality sequence and verify that every command exits with code 0:

```bash
# 1. Format code with Ruff
./pants fmt ::

# 2. Lint code with Ruff
./pants lint ::

# 3. Type check with Mypy
./pants check ::

# 4. Run tests with Pytest
./pants test ::
```

If packaging artifacts (`pex_binary` or `docker_image`), also test the build:
```bash
./pants package <target_address>
```

**Never declare a task done if any of the above commands fail.**
