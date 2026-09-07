python_sources(
    name="core_lib",
    sources=["core/**/*.py"],
    resolve=parametrize("core_resolve", "churn_resolve"),
)

python_tests(
    name="tests",
    sources=["core/**/test_*.py"],
    resolve="core_resolve",
)
