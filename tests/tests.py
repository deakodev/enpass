import unittest
from unittest.mock import patch
from src.en_cli import confirm, cli_args
from src.en_cli import (
    cli_login, cli_logout, cli_add,
    cli_remove, cli_list, cli_view, Result
)
import argparse


class TestEnpassCLI(unittest.TestCase):

    @patch("builtins.input", return_value="Y")
    def test_confirm_yes(self, mock_input):
        self.assertTrue(confirm("Proceed?"))

    @patch("builtins.input", return_value="n")
    def test_confirm_no(self, mock_input):
        self.assertFalse(confirm("Proceed?"))

    @patch("argparse.ArgumentParser.parse_args")
    def test_cli_args(self, mock_parse_args):
        mock_namespace = argparse.Namespace(command="login", master=None, name=None)
        mock_parse_args.return_value = mock_namespace
        args = cli_args()
        self.assertEqual(args.command, "login")

    @patch("en_cli.session_active", return_value=True)
    def test_cli_login_redundant(self, _):
        args = argparse.Namespace(master="any")
        result = cli_login(args)
        self.assertEqual(result, Result.LOGIN_REDUNDANT)

    @patch("en_cli.session_active", return_value=False)
    @patch("en_cli.getpass", return_value="correct_password")
    @patch("en_cli.vault_master_confirm", return_value=True)
    @patch("en_cli.session_start", return_value=True)
    def test_cli_login_success(self, *_):
        args = argparse.Namespace(master=None)
        result = cli_login(args)
        self.assertEqual(result, Result.LOGIN_SUCCESS)

    @patch("en_cli.session_end", return_value=True)
    def test_cli_logout_success(self, _):
        result = cli_logout(None)
        self.assertEqual(result, Result.LOGOUT_SUCCESS)

    @patch("en_cli.session_end", return_value=False)
    def test_cli_logout_redundant(self, _):
        result = cli_logout(None)
        self.assertEqual(result, Result.LOGOUT_REDUNDANT)

    @patch("en_cli.session_active", return_value=False)
    def test_cli_add_inactive(self, _):
        result = cli_add(None)
        self.assertTrue(result & Result.SESSION_INACTIVE)

    @patch("en_cli.session_active", return_value=False)
    def test_cli_remove_inactive(self, _):
        args = argparse.Namespace(name="gmail")
        result = cli_remove(args)
        self.assertTrue(result & Result.SESSION_INACTIVE)

    @patch("en_cli.session_active", return_value=False)
    def test_cli_list_inactive(self, _):
        result = cli_list(None)
        self.assertTrue(result & Result.SESSION_INACTIVE)

    @patch("en_cli.session_active", return_value=False)
    def test_cli_view_inactive(self, _):
        args = argparse.Namespace(name="gmail")
        result = cli_view(args)
        self.assertTrue(result & Result.SESSION_INACTIVE)


if __name__ == "__main__":
    unittest.main()
