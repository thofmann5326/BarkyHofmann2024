# test_barky.py

import pytest
from unittest.mock import patch
from barky import Option, clear_screen, loop


@pytest.fixture
def mock_user_input(monkeypatch):
    user_inputs = []

    def mock_input(prompt):
        print(prompt, end="")
        user_input = user_inputs.pop(0)
        print(user_input)
        return user_input

    monkeypatch.setattr('builtins.input', mock_input)

    return user_inputs


@pytest.fixture
def barky_with_mocked_input(mock_user_input):
    with patch('barky.commands.CreateBookmarksTableCommand.execute'):
        with patch('barky.commands.AddBookmarkCommand.execute'):
            with patch('barky.commands.ListBookmarksCommand.execute'):
                with patch('barky.commands.DeleteBookmarkCommand.execute'):
                    with patch('barky.commands.ImportGitHubStarsCommand.execute'):
                        with patch('barky.commands.EditBookmarkCommand.execute'):
                            with patch('barky.commands.QuitCommand.execute'):
                                yield mock_user_input


def test_barky_add_bookmark(barky_with_mocked_input):
    mock_user_input = barky_with_mocked_input
    mock_user_input.extend(
        ['A', 'New Bookmark', 'http://example.com', 'Some notes', ''])

    with patch('barky.commands.AddBookmarkCommand.execute') as mock_execute:
        loop()

    mock_execute.assert_called_with(
        {'title': 'New Bookmark', 'url': 'http://example.com', 'notes': 'Some notes'})
