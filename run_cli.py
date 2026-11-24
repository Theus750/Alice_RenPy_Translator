import sys

from cli.run_cli import (  # noqa: F401
    _apply_config_overrides,
    _configure_logging,
    _infer_renpy_language,
    _resolve_relative_path,
    build_parser,
    main,
)


if __name__ == "__main__":
    main()