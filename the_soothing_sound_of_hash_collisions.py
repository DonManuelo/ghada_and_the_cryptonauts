#!/usr/bin/env python
"""
    <Name>
        the_soothing_sound_of_hash_collisions

    <Description>
        This is the first hit of ghada and the cryptonauts. The new cryptotune
        promise band (it's like shoegaze but less shoes and more white noise).

    <Usage>
        Run as a program:
            ./the_soothing_sound_of_hash_collisions.py

    <Author>
        Santiago Torres (torresariass@gmail.com)

    <License>
        Beerware, I guess. Do whatever you want with this snippet
"""
import scikits.audiolab as a 
from hashlib import sha1
import time

from numpy import array, pi, sin, arange

DEFAULT_SECONDS = 2
DEFAULT_FREQUENCY = 440.0
DEFAULT_DELAY = 0

"""
    This function loads random values from rand and turns them into a frequency
    and a duration to play the sin beep
"""
def the_soothing_sound_of_hash_collisions():

    # it's a 3 minute song
    song_length = 3*60 

    with open('/dev/urandom', 'rb') as fp:

        while (song_length > 0):
            # we read 32 bits we hash it bc yolo
            this_frame = fp.read(32);
            this_frame = sha1(this_frame).digest()

            # we need 14 bits to map to the audible range, so we will use two bytes
            # and mask it out
            this_note = int(this_frame[:2].encode('hex'), 16)
            frequency = this_note & 0x1FFF;

            # we will choose durations between .2 seconds and 3 seconds to keep
            # things interesting, we have 18 bytes left. This is too much, so we will
            # have to discriminate
            crc = 0
            for i in range(2, 20):
                crc ^= int(this_frame[i].encode('hex'), 16)

            crc &= 0xFF
            crc /= 100.0

            print("playing {} for {} seconds".format(frequency, crc))

            play_sin_beep(crc, frequency)
            song_length -= crc


"""
    Play a beep of the specific frequeny for secs seconds. This beep is 
    a smoother sinusoidal wave (play_beep defaults to a sawtooth).
"""
def play_sin_beep(secs = DEFAULT_SECONDS, notefreq = DEFAULT_FREQUENCY,
        delay = DEFAULT_DELAY):

    # define the length of the beep
    fs = 44100
    vectorstep  = 1/float(fs)

    # create the sinusoidal vector
    sin_vect = sin([2 * pi * notefreq * x for x in arange(0, secs, vectorstep)])
    normalization_const = max(sin_vect)

    beep = array([x/normalization_const for x in sin_vect])

    a.play(beep, fs=fs)
    time.sleep(delay)


if __name__ == "__main__":

    the_soothing_sound_of_hash_collisions()

