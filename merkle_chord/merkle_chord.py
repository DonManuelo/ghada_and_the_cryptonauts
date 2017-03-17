#!/usr/bin/env python
"""
    <Name>
        Merkel chord

    <Description>
        This is the second hit of ghada and the cryptonauts. The new cryptotune
        promise band (it's like shoegaze but less shoes and more white noise).

    <Usage>
        Run as a program:
            ./merkle_chord.py

    <Author>
        Santiago Torres (torresariass@gmail.com)

    <License>
        Beerware, I guess. Do whatever you want with this snippet
"""
import scikits.audiolab as a 
from hashlib import sha256
import time

from numpy import array, pi, sin, arange
import numpy as np

DEFAULT_SECONDS = 8
DEFAULT_FREQUENCY = 440.0
DEFAULT_DELAY = 0

def locate_freq_from_hash(hash):
    """ this function takes a hash value of any length and computes the 
    frequency of a random note in the hardcoded scale """
    Pentacorde       = {"C":16.35,
                        "C#":17.32,
                        "E":20.60,
                        "A":27.50,
                        "G#": 25.96,      
                        "D": 36.71
                        }
    NOTE_KEYS = Pentacorde.keys()

    # we choose between 8 octaves, take the MSNibble to select the octave.
    octave = (int(hash[0].encode('hex'), 16) >> 6) + 2
    octave_multiplier = pow(2, octave)

    # use the rest of the hash too compute the key index;
    crc = 0
    for byte in hash[1:]:
        crc ^= int(byte.encode('hex'), 16);

    crc = crc % len(NOTE_KEYS)

    # obtain the base frequency 
    note_frequency = Pentacorde[NOTE_KEYS[crc]] * octave_multiplier;
    return note_frequency

def compute_frequencies_for_tree_level(hash_nodes):
    """ Returns a list of frequencies of the length of hash_nodes """ 
    these_frequencies = [] 

    for this_frame in hash_nodes:

        # now, obtain a note out of it
        this_note = locate_freq_from_hash(this_frame)
        these_frequencies.append(this_note)

    return these_frequencies

def compute_and_flatten_notes(frame_frequency, seconds_length):

    pcm_frames = []
    for freq in frame_frequency:
        pcm_frame = play_sin_beep(seconds_length, freq)

        pcm_frames.append(pcm_frame)

    # sum normalize everything to 1
    frame_pcm = np.sum(np.array(pcm_frames), axis=0)
    normalization_const = max(frame_pcm)

    return array([x/normalization_const for x in frame_pcm])


def compute_tree_level(round_hashes):

    new_round = []
    print(len(round_hashes))
    if (len(round_hashes) == 1):
        return new_round
    for i in range(0, len(round_hashes), 2):
        this_hash = sha256(round_hashes[i])
        this_hash.update(round_hashes[i+1])
        new_round.append(this_hash.digest())

    return new_round

"""
    This function loads random values from rand and turns them into a frequency
    and a duration to play the sin beep
"""
def the_soothing_sound_of_hash_collisions():

    # it's a 3 minute song
    SECONDS_PER_FRAME = 8
    TREE_SIZE = 256

    frames = []
    with open('/dev/urandom', 'rb') as fp:

        output = a.sndfile("merkle_chord.wav", format=a.formatinfo(),
                mode='write', channels=1, samplerate=44100)
        
        round_size = TREE_SIZE;
        round_hashes  = []

        # we will seed this with 2 * TREE_SIZE random values that will be used
        # by the algorithm to compute the leaves
        for i in range(0, TREE_SIZE * 2):
            this_seed = fp.read(32)
            round_hashes.append(this_seed)

        while (True):

            round_hashes = compute_tree_level(round_hashes)

            # we exhausted the tree by now
            if not round_hashes:
                break

            frame_frequencies = compute_frequencies_for_tree_level(round_hashes)
            print(frame_frequencies)
            
            frame_pcm = compute_and_flatten_notes(frame_frequencies,
                    SECONDS_PER_FRAME)

            output.write_frames(frame_pcm)

        output.sync()


"""
    Play a beep of the specific frequeny for secs seconds. This beep is 
    a smoother sinusoidal wave (play_beep defaults to a sawtooth).
"""
def play_sin_beep(secs = DEFAULT_SECONDS, notefreq = DEFAULT_FREQUENCY):

    # define the length of the beep
    fs = 44100
    vectorstep  = 1/float(fs)

    # create the sinusoidal vector
    sin_vect = sin([2 * pi * notefreq * x for x in arange(0, secs, vectorstep)])
    normalization_const = max(sin_vect)

    beep = array([x/normalization_const for x in sin_vect])

    #a.play(beep, fs=fs)
    return beep


if __name__ == "__main__":

    the_soothing_sound_of_hash_collisions()

