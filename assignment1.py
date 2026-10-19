"""
Name:XU TAISHUO
Date started:10/18
GitHub URL:https://github.com/Xutaishuo/CP1404_assignment

"""
import random
from operator import itemgetter

SONGS_FILE = "songs.csv"

TITLE_INDEX = 0
ARTIST_INDEX = 1
YEAR_INDEX = 2
LEARNED_INDEX = 3

LEARNED = "l"
UNLEARNED = "u"
UNLEARNED_MARKER = "*"
CLASSIC_YEAR = 1975

MENU = """D - Display songs
R - Recommend a random song
A - Add a new song
C - Complete a song
Q - Quit"""
def main():    
    print("Song Supply 1.0 - by XU TAISHUO")
    while True:
        print(MENU)
        choice = input(">>> ").upper()
        if choice == "D":
            display_songs(songs)
        elif choice == "R":
            recommend_song(songs)
        elif choice == "A":
            add_song(songs)
        elif choice == "C":
            complete_song(songs)
        elif choice == "Q":
            save_songs(songs, SONGS_FILE)
            print("Enjoy the music!")
            break
        else:
            print("Invalid menu choice")
def load_songs(filename):
    songs = []
    try:
        with open(filename, "r") as in_file:
            for line in in_file:
                line = line.strip()
                if line == "":
                    continue
                parts = line.split(",")
                title = parts[TITLE_INDEX].strip()
                artist = parts[ARTIST_INDEX].strip()
                year = int(parts[YEAR_INDEX].strip())
                learned = parts[LEARNED_INDEX].strip()
                songs.append([title, artist, year, learned])
    except FileNotFoundError:
        print(f"ERROR: '{filename}' not found")
    return songs
def save_songs(songs, filename):
    """Save all songs to a CSV file."""
    with open(filename, "w") as out_file:
        for song in songs:
            out_file.write(
                f"{song[TITLE_INDEX]},{song[ARTIST_INDEX]},"
                f"{song[YEAR_INDEX]},{song[LEARNED_INDEX]}\n"
            )
    print(f"{len(songs)} songs saved to {filename}")


def display_songs(songs):
    if not songs:
        print("No songs")
        return

    sorted_songs = sorted(songs, key=itemgetter(YEAR_INDEX, TITLE_INDEX))
    learned_count = 0

    for number, song in enumerate(sorted_songs, 1):
        if song[LEARNED_INDEX] == LEARNED:
            marker = ""
            learned_count += 1
        else:
            marker = f"{UNLEARNED_MARKER} "

        classic_text = ""

        if song[YEAR_INDEX] <= CLASSIC_YEAR:
            classic_text = " (classic)"

        print(
            f"{number}. {marker}{song[TITLE_INDEX]} - "
            f"{song[ARTIST_INDEX]} {song[YEAR_INDEX]}{classic_text}"
        )

    unlearned_count = len(songs) - learned_count
    print(f"{learned_count} songs learned, {unlearned_count} songs still to learn")


def recommend_song(songs):
    unlearned_songs = []
    for song in songs:
        if song[LEARNED_INDEX] == UNLEARNED:
            unlearned_songs.append(song)

    if not unlearned_songs:
        print("No songs to learn")
    else:
        song = random.choice(unlearned_songs)
        print(f"Let's learn... {song[TITLE_INDEX]} by {song[ARTIST_INDEX]}")


def add_song(songs):
    print("Enter details for a new song.")
    title = get_valid_string("Title: ")
    artist = get_valid_string("Artist: ")
    year = get_valid_integer("Year: ", 1)

    songs.append([title, artist, year, UNLEARNED])
    print(f"{title} by {artist} ({year}) added to song list")


def complete_song(songs):
    has_unlearned = False
    for song in songs:
        if song[LEARNED_INDEX] == UNLEARNED:
            has_unlearned = True
            break

    if not has_unlearned:
        print("No unlearned songs")
        return

    print("Enter the number of a song to mark as learned")
    sorted_songs = sorted(songs, key=itemgetter(YEAR_INDEX, TITLE_INDEX))

    while True:
        song_number = get_valid_integer(">>> ", 1, len(sorted_songs))
        song = sorted_songs[song_number - 1]

        if song[LEARNED_INDEX] == LEARNED:
            print("Song is already learned")
        else:
            song[LEARNED_INDEX] = LEARNED
            print(f"{song[TITLE_INDEX]} by {song[ARTIST_INDEX]} learned")
            return


def get_valid_string(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input can not be blank")


def get_valid_integer(prompt, minimum, maximum=None):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Enter a valid integer")
        else:
            if value < minimum:
                print("Number must be > 0")
            elif maximum is not None and value > maximum:
                print("Invalid song number")
            else:
                return value


if __name__ == "__main__":
    main()
