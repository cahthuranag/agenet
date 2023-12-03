# Development

## Installing for development and/or improving the package

```text
$ git clone https://github.com/cahthuranag/agenet.git
$ cd agenet
$ python -m venv env
$ source env/bin/activate
$ pip install -e .[dev]
$ pre-commit install
```

On Windows replace `source env/bin/activate` with `. env\Scripts\activate`.

## Run tests

Tests can be executed with the following command:

```text
$ pytest
```

The previous command runs the tests at `normal` level by default. This test
level can also be specified explicitly:

```text
$ pytest --test-level=normal
```



To generate a test coverage report, run pytest as follows:

```text
$ pytest --cov=agenet --cov-report=html --test-level=ci
```

## Build docs

Considering we're in the `agenet` folder, run the following commands:

```text
$ cd docs
$ mkdocs build
```

The generated documentation will be placed in `docs/site`. Alternatively, the
documentation can be generated and served locally with:

```
$ mkdocs serve
```

## Code style

Code style is enforced with [flake8] (and a number of plugins), [black], and
[isort]. Some highlights include, but are not limited to:

* Encoding: UTF-8
* Indentation: 4 spaces (no tabs)
* Line size limit: 88 chars
* Newlines: Unix style, i.e. LF or \n

[black]: https://black.readthedocs.io/en/stable/
[flake8]: https://flake8.pycqa.org/en/latest/
[isort]: https://pycqa.github.io/isort/
