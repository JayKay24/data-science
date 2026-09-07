# Data Science Monorepo (Pantsbuild)

A modern, high-performance Pantsbuild monorepo designed for data science and machine learning portfolio projects.

## Architecture & Features

- **Pants Build System**: Fast hermetic builds, fine-grained target-level caching, and automatic dependency inference.
- **Multiple Resolves**: Distinct dependency lockfiles per project and shared libraries to prevent version conflicts across heavy ML frameworks (e.g. Scikit-learn, PyTorch, PySpark).
- **Code Quality Stack**:
  - **Ruff**: Ultra-fast linting and formatting.
  - **Mypy**: Strict static type checking.
  - **Pytest**: Parallelized unit and integration testing with Pants caching.
  - **Jupyter Notebook Support**: Pants-integrated linting for `.ipynb` exploration notebooks.
- **Packaging & Deployment**:
  - **PEX Standalone Executables**: Self-contained Python binaries built via `./pants package`.
  - **Docker Containers**: Ready for containerized API and model serving.

---

## Directory Structure

```text
├── 3rdparty/
│   └── python/
│       ├── BUILD                    # python_requirements for each resolve
│       ├── core-requirements.txt    # Shared library requirements
│       ├── churn-requirements.txt   # Churn project requirements
│       ├── core.lock                # Generated hermetic lockfile for core
│       └── churn.lock               # Generated hermetic lockfile for churn
├── libs/
│   └── core/                        # Shared utility library (metrics, preprocessing)
│       ├── BUILD
│       └── core/
│           ├── metrics.py
│           ├── preprocessing.py
│           └── test_metrics.py
├── projects/
│   └── churn_prediction/            # Sample ML portfolio project
│       ├── BUILD
│       ├── Dockerfile
│       ├── churn_prediction/
│       │   ├── app.py               # FastAPI model serving endpoint
│       │   ├── features.py          # Data generation & feature transformation
│       │   ├── train.py             # Model training pipeline
│       │   └── tests/               # Pytest test suite
│       └── notebooks/
│           └── exploration.ipynb    # Exploratory analysis notebook
├── pants                            # Scie-pants self-contained launcher
├── pants.toml                       # Pants build system configuration
├── mypy.ini                         # Mypy type-checking configuration
└── .gitignore
```

---

## Getting Started

The repository comes with the `./pants` launcher script already included.

### 1. Run Unit Tests (Target-Based)
```bash
# Run all tests in repository
./pants test ::

# Run specific project tests
./pants test projects/churn_prediction:tests

# Run shared library tests
./pants test libs/core:tests
```

### 2. Format & Lint
```bash
# Format code (Ruff)
./pants fmt ::

# Lint code (Ruff)
./pants lint ::

# Typecheck (Mypy)
./pants check ::
```

### 3. Package & Run Executables
```bash
# Package standalone PEX binary
./pants package projects/churn_prediction:train_bin

# Execute the resulting standalone binary
./dist/projects.churn_prediction/train_bin.pex

# Package FastAPI serving binary
./pants package projects/churn_prediction:churn_service

# Run FastAPI server
./dist/projects.churn_prediction/churn_service.pex
```

### 4. Dependency Updates & Lockfiles
Whenever you modify `3rdparty/python/*-requirements.txt`, regenerate the hermetic lockfiles:
```bash
./pants generate-lockfiles
```

---

## Adding a New Project

1. Create your project directory: `mkdir -p projects/<project_name>/<project_name>`
2. Define dependencies in `3rdparty/python/<project_name>-requirements.txt` and register the resolve in `pants.toml` and `3rdparty/python/BUILD`.
3. Add a `BUILD` file inside `projects/<project_name>/BUILD` with `python_sources`, `python_tests`, and optional `pex_binary` / `docker_image` targets.
4. Run `./pants generate-lockfiles` to generate its lockfile.
