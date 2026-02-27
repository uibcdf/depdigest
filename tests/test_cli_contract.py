import pytest

from depdigest.cli import main


def test_cli_without_subcommand_returns_zero(capsys):
    rc = main([])
    captured = capsys.readouterr()
    assert rc == 0
    assert "usage:" in captured.out.lower()


def test_cli_rejects_missing_soft_deps_argument():
    with pytest.raises(SystemExit):
        main(["audit", "--src-root", "."])


def test_cli_rejects_empty_soft_deps_values():
    with pytest.raises(SystemExit):
        main(["audit", "--src-root", ".", "--soft-deps", " , "])

