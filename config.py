import pygame
import random
import os
import time
import curses

SOUND_FOLDER = "sounds"
STATE_TRANSITION_CHANCE = 0.05
SUB_STATE_TRANSITION_CHANCE = 0.08

# Main sounds
MAIN_SOUND = "crowded_tavern.mp3"
GLASS_SHATER_SOUNDS = os.listdir(SOUND_FOLDER + "/glass_shater")
LAUGH_SOUNDS = os.listdir(SOUND_FOLDER + "/laugh")
WHISPER_SOUNDS = os.listdir(SOUND_FOLDER + "/whisper")
RANDOM_SOUNDS = os.listdir(SOUND_FOLDER + "/random")

# Fight sounds
BRAWL_SOUND = "brawl.mp3"
FIGHT_SOUNDS = os.listdir(SOUND_FOLDER + "/fight")
WISTLE_SOUNDS = os.listdir(SOUND_FOLDER + "/wistle")
SCREAM_SOUNDS = os.listdir(SOUND_FOLDER + "/scream")

# Music sounds
MUSIC_SOUNDS = os.listdir(SOUND_FOLDER + "/music")
SHH_SOUNDS = os.listdir(SOUND_FOLDER + "/shh")
CHEERING_SOUNDS = os.listdir(SOUND_FOLDER + "/cheering")

# Conversation
CONV_SOUNDS = os.listdir(SOUND_FOLDER + "/conversation")


# Banner
BANNER = [
"""
████████╗
╚══██╔══╝
   ██║
   ██║
   ██║
   ╚═╝   """,
"""
 █████╗
██╔══██╗
███████║
██╔══██║
██║  ██║
╚═╝  ╚═╝""",
"""
██╗   ██╗
██║   ██║
██║   ██║
╚██╗ ██╔╝
 ╚████╔╝
  ╚═══╝ """,
"""
███████╗
██╔════╝
█████╗
██╔══╝
███████╗
╚══════╝""",
"""
██████╗
██╔══██╗
██████╔╝
██╔══██╗
██║  ██║
╚═╝  ╚═╝""",
"""
███╗   ██╗
████╗  ██║
██╔██╗ ██║
██║╚██╗██║
██║ ╚████║
╚═╝  ╚═══╝""",
"""
██╗
██║
██║
██║
██║
╚═╝""",
"""
███╗   ██╗
████╗  ██║
██╔██╗ ██║
██║╚██╗██║
██║ ╚████║
╚═╝  ╚═══╝""",
"""





   v1.0 by Valenwe
"""
]

def load_sounds():
    main_sound = {MAIN_SOUND: pygame.mixer.Sound(f"{SOUND_FOLDER}/{MAIN_SOUND}")}
    glass_shatter_sounds = {sound: pygame.mixer.Sound(f"{SOUND_FOLDER}/glass_shater/{sound}") for sound in GLASS_SHATER_SOUNDS}
    whisper_sounds = {sound: pygame.mixer.Sound(f"{SOUND_FOLDER}/whisper/{sound}") for sound in WHISPER_SOUNDS}
    random_sounds = {sound: pygame.mixer.Sound(f"{SOUND_FOLDER}/random/{sound}") for sound in RANDOM_SOUNDS}
    laugh_sounds = {sound: pygame.mixer.Sound(f"{SOUND_FOLDER}/laugh/{sound}") for sound in LAUGH_SOUNDS}

    music_sounds = {sound: pygame.mixer.Sound(f"{SOUND_FOLDER}/music/{sound}") for sound in MUSIC_SOUNDS}
    shh_sounds = {sound: pygame.mixer.Sound(f"{SOUND_FOLDER}/shh/{sound}") for sound in SHH_SOUNDS}
    cheering_sounds = {sound: pygame.mixer.Sound(f"{SOUND_FOLDER}/cheering/{sound}") for sound in CHEERING_SOUNDS}

    brawl_sound = {BRAWL_SOUND: pygame.mixer.Sound(f"{SOUND_FOLDER}/{BRAWL_SOUND}")}
    wistle_sounds = {sound: pygame.mixer.Sound(f"{SOUND_FOLDER}/wistle/{sound}") for sound in WISTLE_SOUNDS}
    fight_sounds = {sound: pygame.mixer.Sound(f"{SOUND_FOLDER}/fight/{sound}") for sound in FIGHT_SOUNDS}
    scream_sounds = {sound: pygame.mixer.Sound(f"{SOUND_FOLDER}/scream/{sound}") for sound in SCREAM_SOUNDS}

    conv_sounds = {sound: pygame.mixer.Sound(f"{SOUND_FOLDER}/conversation/{sound}") for sound in CONV_SOUNDS}

    return (main_sound, glass_shatter_sounds, whisper_sounds, random_sounds, music_sounds, shh_sounds
            , cheering_sounds, brawl_sound, wistle_sounds, fight_sounds, scream_sounds
            , conv_sounds, laugh_sounds)

def get_random_sound(sound_dict: dict, previous_played_sounds: list):
    possibles_keys = list(sound_dict.keys())

    # remove previous sounds
    if len(possibles_keys) > 2:
        possibles_keys = [item for item in possibles_keys if item not in previous_played_sounds]

    random_key = random.choice(possibles_keys)
    random_sound = sound_dict[random_key]
    return random_key, random_sound

def print_and_flush(stdscr, message):
    # Clear the line
    stdscr.addstr(0, 0, " " * curses.COLS)
    stdscr.refresh()

    # Print the new message
    stdscr.addstr(0, 0, message)
    stdscr.refresh()

def get_banner_printing(stdscr):
    curses.curs_set(0)
    first = pygame.mixer.Sound(f"{SOUND_FOLDER}/banner/first.mp3")
    second = pygame.mixer.Sound(f"{SOUND_FOLDER}/banner/second.mp3")
    last = pygame.mixer.Sound(f"{SOUND_FOLDER}/banner/last.mp3")
    maximum_line_nb = len(BANNER[0].split("\n")) - 1
    word = "\n" * maximum_line_nb

    for i in range(len(BANNER)):
        letter = BANNER[i]

        new_word = ""
        letter_lines = letter.split("\n")
        word_lines = word.split("\n")
        maximum_line_length = max([len(line) for line in word_lines])

        while len(letter_lines) < maximum_line_nb:
            letter_lines.append("\n")

        for I in range(len(word_lines)):
            new_word += word_lines[I].ljust(maximum_line_length) + letter_lines[I] + ("\n" if I < len(word_lines) - 1 else "")

        word = new_word
        channel = pygame.mixer.find_channel(True)

        if i < len(BANNER) - 1:
            time.sleep(0.15)

            if channel:
                if i == 0:
                    channel.play(first, fade_ms=200)
                else:
                    channel.play(second, fade_ms=200)
            print_and_flush(stdscr, word)

        else:
            time.sleep(0.6)
            if channel:
                channel.play(last, fade_ms=200)
            print_and_flush(stdscr, word)
            print("")
            time.sleep(0.5)
    return word

def print_banner():
    word = curses.wrapper(get_banner_printing)
    curses.endwin()
    print(word)