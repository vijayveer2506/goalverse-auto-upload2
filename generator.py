import random
from utils import (
    random_line,
    load_used_titles,
    save_used_title,
)


def generate_title(channel_name):

    used = load_used_titles()

    for _ in range(100):

        opening = random_line("openings.txt", "🔥 Amazing")

        subject_pool = [
            random_line("subjects.txt", "Football Moment"),
            random_line("players.txt", "Football"),
            random_line("competitions.txt", "Champions League"),
        ]

        subject = random.choice(subject_pool)

        ending = random_line("endings.txt", "You Must See!")

        title = f"{opening} {subject} {ending}"

        title = " ".join(title.split())

        if len(title) > 100:
            title = title[:100]

        if title not in used:
            save_used_title(title)
            return title

    return f"{channel_name} Football Shorts"


def generate_description(channel_name):

    intro = random_line(
        "descriptions.txt",
        f"Welcome to {channel_name}!"
    )

    hashtags = random_line(
        "hashtags.txt",
        "#football #soccer #shorts"
    )

    description = f"""{intro}

⚽ Daily Football Shorts

🔥 Goals
⚡ Skills
🧤 Saves
🏆 Highlights
🎯 Free Kicks

👍 Like
💬 Comment
🔔 Subscribe

{hashtags}
"""

    return description


def generate_hashtags():

    return random_line(
        "hashtags.txt",
        "#football #soccer #shorts"
    )
