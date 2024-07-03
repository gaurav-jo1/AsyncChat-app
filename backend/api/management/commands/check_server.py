from django.core.management.base import BaseCommand
from django.db import connections
import time

class Command(BaseCommand):
    help = "Starts the Django development server only if the database is available."

    def handle(self, *args, **options):
        self.stdout.write("🛸 Checking database availability...")
        db_conn = None
        max_attempts = 10  # Adjust the number of attempts as needed
        attempts = 0

        while not db_conn and attempts < max_attempts:
            try:
                db_conn = connections['default']
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Database is not available: {e}"))
                self.stdout.write("Server not started, waiting for 1 sec....")
                time.sleep(1)
                attempts += 1

        if db_conn:
            self.stdout.write("🚀 Database is available. Starting the server...")
        else:
            self.stdout.write(self.style.ERROR('🔥 Unable to connect to the database.'))
            raise SystemExit(1)
