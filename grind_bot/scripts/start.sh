curl -sSL https://install.python-poetry.org | python
~/.local/bin/poetry install --with psql --with debug
cd ~
~/.local/bin/poetry run alembic upgrade head
echo 'upgraded'
# ~/.local/bin/poetry run pytest
# echo 'tests finished'
~/.local/bin/poetry run start