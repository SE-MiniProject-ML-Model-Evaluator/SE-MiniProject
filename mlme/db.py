"""SQLite tuning for concurrent users (NFR-03): WAL mode lets readers and a writer work at the same time."""
from django.db.backends.signals import connection_created
from django.dispatch import receiver


@receiver(connection_created)
def sqlite_pragmas(sender, connection, **kwargs):
    if connection.vendor == "sqlite":
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA synchronous=NORMAL;")
