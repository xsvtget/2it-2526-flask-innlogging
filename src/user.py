from dataclasses import dataclass
from src.auth import hash_password, is_correct_password
import sqlite3

DATABASE = "test.db"


@dataclass
class User:
    username: str
    password: str
    fornavn: str
    etternavn: str
    _load_from_db: bool = False

    def __post_init__(self):
        if self._load_from_db:
            return
        self.username = self.username.lower()
        self.password = hash_password(self.password, self.username)
        self.save_to_db()

    def save_to_db(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (
                username,
                password,
                fornavn,
                etternavn
            ) VALUES (
                :username,
                :password,
                :fornavn,
                :etternavn
            )
            """,
            {
                "username": self.username,
                "password": self.password,
                "fornavn": self.fornavn,
                "etternavn": self.etternavn,
            },
        )
        conn.commit()
        conn.close()

    def check_password(self, password: str) -> bool:
        return is_correct_password(password, self.username, self.password)

    @property
    def fullt_navn(self):
        return f"{self.fornavn} {self.etternavn}"


def get_all() -> dict[str, User]:
    data = {}

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")

    for row in cursor.fetchall():
        data[row[0]] = User(*row, _load_from_db=True)

    conn.close()
    return data


def get(username: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username.lower(),))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return User(*row, _load_from_db=True)


def add_note(username: str, content: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO notes (username, content)
        VALUES (?, ?)
        """,
        (username.lower(), content),
    )
    conn.commit()
    conn.close()


def get_notes_by_user(username: str):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, username, content, created_at
        FROM notes
        WHERE username = ?
        ORDER BY created_at DESC, id DESC
        """,
        (username.lower(),),
    )
    notes = cursor.fetchall()
    conn.close()
    return notes


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            fornavn TEXT,
            etternavn TEXT,
            UNIQUE(username)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username)
        )
        """
    )

    conn.commit()
    conn.close()


init_db()