"""Account storage for login and name changes; compatible with legacy main rows."""
import json
from pathlib import Path
import secrets
import sqlite3

from Classes.Instances.Classes.Player import Player

_DATABASE_PATH = Path(__file__).resolve().parent / 'Files' / 'player.sqlite'


class DatabaseHandler:
    def __init__(self, path=None):
        path = Path(path) if path is not None else _DATABASE_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path, timeout=5)
        try:
            self.conn.execute('PRAGMA journal_mode=WAL')
            self.conn.execute('PRAGMA synchronous=NORMAL')
            with self.conn:
                self.conn.execute('CREATE TABLE IF NOT EXISTS main (ID int, Token text, Data json)')
                self.conn.execute('CREATE INDEX IF NOT EXISTS idx_player_main_id ON main(ID)')
        except Exception:
            self.conn.close()
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def login(self, account_id, token):
        """Authenticate an existing account or allocate the next ID if absent."""
        high, low = account_id
        if high == 0 and low > 0:
            row = self.conn.execute(
                'SELECT ID, Token, Data FROM main WHERE ID=?', (low,)
            ).fetchone()
            if row is not None:
                if not token or row[1] != token:
                    return None
                data = json.loads(row[2])
                return Player(ID=[0, row[0]], Token=row[1],
                              Name=data.get('Name', '@BSVSCHANNEL'),
                              Registered=bool(data.get('Registered', False)))

        # Allocate the ID and insert under one write lock, including across processes.
        with self.conn:
            self.conn.execute('BEGIN IMMEDIATE')
            low = self.conn.execute('SELECT COALESCE(MAX(ID), 0) + 1 FROM main').fetchone()[0]
            player = Player(ID=[0, low], Token=secrets.token_urlsafe(30))
            data = {'ID': player.ID, 'Token': player.Token,
                    'Name': player.Name, 'Registered': player.Registered}
            self.conn.execute('INSERT INTO main (ID, Token, Data) VALUES (?, ?, ?)',
                              (low, player.Token, json.dumps(data, ensure_ascii=False, separators=(',', ':'))))
        return player

    def set_name(self, player, name):
        """Commit the name before acknowledging it; preserve legacy JSON fields."""
        if player.ID[1] == 0:
            return False
        with self.conn:
            self.conn.execute('BEGIN IMMEDIATE')
            row = self.conn.execute(
                'SELECT Data FROM main WHERE ID=? AND Token=?',
                (player.ID[1], player.Token),
            ).fetchone()
            if row is None:
                return False
            data = json.loads(row[0])
            data['Name'] = name
            data['Registered'] = True
            self.conn.execute('UPDATE main SET Data=? WHERE ID=? AND Token=?',
                              (json.dumps(data, ensure_ascii=False, separators=(',', ':')),
                               player.ID[1], player.Token))
        player.Name = name
        player.Registered = True
        return True
