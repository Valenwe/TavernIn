import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import time
import logging
from threading import Thread
from state import *
from config import *

def play_main_sound(main_sound: tuple[str, pygame.mixer.Sound]):
    """Plays the main constant sound
    """
    main_channel = pygame.mixer.Channel(0)
    main_channel.fadeout(3000)
    main_channel.play(main_sound, loops=-1, fade_ms=3000)  # -1 loops indefinitely

def play_additional_sound(sound: tuple[str, pygame.mixer.Sound], volume=1.0, end_percentage=None, back_to_default=False):
    """play_additional_sound
    Will play any given sound in a separate thread
    """
    def play_sound_thread(sound: tuple[str, pygame.mixer.Sound], volume=1.0, end_percentage=None, back_to_default=False):
        filename = sound[0]
        sound_mixer = sound[1]

        # update the last played sounds
        global previous_played_sounds
        if len(previous_played_sounds) == 2:
            previous_played_sounds.pop()
        previous_played_sounds = [filename] + previous_played_sounds

        end_percentage = 100 if end_percentage is None else end_percentage

        logging.info(f"Playing {filename} (volume: {volume}, end: {end_percentage}%)")

        total_duration = sound_mixer.get_length()
        end_time = total_duration * (end_percentage / 100)

        # Play the sound
        channel = pygame.mixer.find_channel(True)
        if channel:
            channel.set_volume(volume)
            channel.play(sound_mixer, fade_ms=500)

            # Get the start time
            start_time = pygame.time.get_ticks()

            # Wait for the sound to finish playing or reach the desired percentage
            while channel.get_busy():
                elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
                if elapsed_time >= end_time:
                    break
                pygame.time.Clock().tick(60)

            channel.fadeout(1000)

            if back_to_default:
                change_state_to_default(state)
        else:
            logging.error("Could not find an available channel.")

    # Create a new thread for playing the sound
    sound_thread = Thread(target=play_sound_thread, args=(sound, volume, end_percentage, back_to_default,))
    sound_thread.start()

def change_state_to_default(state: StateMachine):
    """change_state_to_default
    Will set the state to default, while playing extra sounds
    """
    random_val = random.randrange(1, 100)

    if random_val < 25:
        volume = random.randrange(80, 100) / 100
        if state.current_state == State.MUSIC:
            play_additional_sound(get_random_sound(cheering_sounds, previous_played_sounds), volume=volume)
        elif state.current_state == State.BRAWL:
            play_additional_sound(get_random_sound(wistle_sounds, previous_played_sounds), volume=volume)
            play_additional_sound(get_random_sound(shh_sounds, previous_played_sounds), volume=volume)

    state.back_to_default()

def state_behavior(state: StateMachine):

    """Will play the main sound depending on the state
    """
    volume = random.randrange(80, 100) / 100
    if state.current_state == State.BRAWL:
        duration = random.randrange(20, 50)
        play_additional_sound(get_random_sound(scream_sounds, previous_played_sounds), volume=volume)
        play_additional_sound((BRAWL_SOUND, brawl_sound[BRAWL_SOUND]), volume=volume, end_percentage=duration, back_to_default=True)
    elif state.current_state == State.MUSIC:
        play_additional_sound(get_random_sound(music_sounds, previous_played_sounds), volume=volume, back_to_default=True)
    elif state.current_state == State.CONVERSATION:
        play_additional_sound(get_random_sound(conv_sounds, previous_played_sounds), volume=1.0, back_to_default=True)

def sub_state_behavior(state: StateMachine):
    """sub_state_behavior
    Will play secondary sounds adapted with the main state
    """
    logging.info("Substate triggered.")
    volume = random.randrange(60, 90) / 100
    if state.current_state == State.BRAWL:
        play_additional_sound(get_random_sound(sub_behavior_brawl, previous_played_sounds), volume=volume)
    elif state.current_state == State.MUSIC:
        play_additional_sound(get_random_sound(sub_behavior_music, previous_played_sounds), volume=volume)
    elif state.current_state in [State.CALM, State.CONVERSATION]:
        play_additional_sound(get_random_sound(sub_behavior_calm, previous_played_sounds), volume=volume)


logging.basicConfig(level=logging.INFO)
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, buffer=2048)
pygame.mixer.set_num_channels(12)

print_banner()

logging.info("Loading soundfiles...")
(main_sound, glass_shatter_sounds, whisper_sounds, random_sounds, music_sounds, shh_sounds
            , cheering_sounds, brawl_sound, wistle_sounds, fight_sounds, scream_sounds
            , conv_sounds, laugh_sounds) = load_sounds()

# sub sounds for the fights
sub_behavior_brawl = dict(wistle_sounds)
sub_behavior_brawl.update(fight_sounds)
sub_behavior_brawl.update(scream_sounds)

# sub sounds for the calm / conversations
sub_behavior_calm = dict(glass_shatter_sounds)
sub_behavior_calm.update(whisper_sounds)
sub_behavior_calm.update(random_sounds)
sub_behavior_calm.update(laugh_sounds)

# sub sounds for the music
sub_behavior_music = dict(shh_sounds)
sub_behavior_music.update(laugh_sounds)

play_main_sound(main_sound[MAIN_SOUND])

state = StateMachine()
logging.info("Starting loop...")

maximum_chance_integer = max([int(1 / chance) for chance in [STATE_TRANSITION_CHANCE, SUB_STATE_TRANSITION_CHANCE]])
global previous_played_sounds
previous_played_sounds = []

try:
    while True:

        random_val = random.randrange(1, maximum_chance_integer)
        # logging.info(f"{random_val}/{maximum_chance_integer}", STATE_TRANSITION_CHANCE * maximum_chance_integer)
        if state.can_transition() and random_val <= STATE_TRANSITION_CHANCE * maximum_chance_integer:
            state.random_transition()
            state_behavior(state)

        if random_val <= SUB_STATE_TRANSITION_CHANCE * maximum_chance_integer:
            sub_state_behavior(state)

        time.sleep(1)

except KeyboardInterrupt:
    pygame.quit()