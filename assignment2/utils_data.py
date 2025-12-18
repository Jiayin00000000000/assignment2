import json
import os

def load_data():
    health_data = {}
    profile = {}

    if os.path.exists("health_data.json"):
        with open("health_data.json", "r") as f:
            health_data = json.load(f)

    if os.path.exists("user_profile.json"):
        with open("user_profile.json", "r") as f:
            profile = json.load(f)

    return health_data, profile


def save_data(health_data, profile):
    with open("health_data.json", "w") as f:
        json.dump(health_data, f, indent=4)

    with open("user_profile.json", "w") as f:
        json.dump(profile, f, indent=4)