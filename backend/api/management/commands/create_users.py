import os
from django.core.management.base import BaseCommand
import json
from django.conf import settings
from django.contrib.auth.models import User
from user_profile.models import User_profile


class Command(BaseCommand):
    help = "Create initial users and their profiles if they don't exist."

    def handle(self, *args, **options):
        user_file_path = os.path.join(settings.BASE_DIR, "user_data.json")

        print("Loading Users:")
        self.import_users_from_json(user_file_path)

    def import_users_from_json(self, json_file_path):
        with open(json_file_path, "r") as file:
            data = json.load(file)

            for user_data in data:
                # Check if a user with the same 'username' already exists in the database
                username = user_data["username"]
                email = user_data["email"]

                existing_user = User.objects.filter(username=username).first()

                if existing_user is None:
                    # Create a new instance of the User model and populate fields from the JSON data
                    new_user = User(
                        username=username,
                        email=email,
                        first_name=user_data["first_name"],
                        last_name=user_data["last_name"],
                    )
                    new_user.set_password(
                        user_data["password"]
                    )  # Make sure passwords are hashed
                    new_user.save()

                    # Create user profile
                    new_profile = User_profile(
                        user=new_user,
                        avatar=user_data.get(
                            "avatar", None
                        ),
                    )
                    new_profile.save()

                    print(f"Inserted user with username: {username}")
                else:
                    print(f"Skipped duplicate user with username: {username}")
