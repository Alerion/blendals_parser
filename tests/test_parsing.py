from pathlib import Path

from rich import print

from blendals_parser.live_set import (
    LiveSet,
    MidiTrack,
    MidiClip,
    Loop,
    TimeSignature,
    KeyTrack,
    MidiNote,
)
from blendals_parser.live_set_parser import LiveSetParser


def get_als_file(file_name: str) -> Path:
    p = Path(__file__).resolve().parent
    return p / "ableton_projects" / file_name


def test_parsing_als_project():
    als_file = get_als_file("Piano Phase v.3 debug (17.04.2024).als")
    live_set_parser = LiveSetParser(als_file)
    live_set = live_set_parser.get_live_set()

    assert live_set == LiveSet(
        name="Piano Phase v.3 debug (17.04.2024)",
        bpm=136,
        time_signature_numerator=4,
        time_signature_denominator=4,
        length_in_bars=1,
        locators=[],
        midi_tracks=[
            MidiTrack(
                name="Main",
                has_drum_rack=False,
                drum_ruck_branches=[],
                midi_clips=[
                    MidiClip(
                        id="4",
                        start=0.0,
                        end=8. * 4,
                        loop=Loop(start=0.0, end=4.0, enabled=True),
                        time_signature=TimeSignature(numerator=4, denominator=4),
                        key_tracks=[
                            KeyTrack(
                                id="40",
                                midi_key=64,
                                midi_notes=[
                                    MidiNote(
                                        time=0.0,
                                        duration=0.3333333333333333,
                                        velocity=90,
                                        midi_key=64,
                                    ),
                                    MidiNote(
                                        time=2.0,
                                        duration=0.3333333333333333,
                                        velocity=90,
                                        midi_key=64,
                                    ),
                                ],
                            ),
                            KeyTrack(
                                id="41",
                                midi_key=65,
                                midi_notes=[
                                    MidiNote(
                                        time=1.6666666666666667,
                                        duration=0.3333333333333333,
                                        velocity=90,
                                        midi_key=65,
                                    ),
                                    MidiNote(
                                        time=3.0,
                                        duration=0.3333333333333333,
                                        velocity=90,
                                        midi_key=65,
                                    ),
                                ],
                            ),
                            KeyTrack(
                                id="42",
                                midi_key=66,
                                midi_notes=[
                                    MidiNote(
                                        time=0.3333333333333333,
                                        duration=0.3333333333333333,
                                        velocity=90,
                                        midi_key=66,
                                    )
                                ],
                            ),
                            KeyTrack(
                                id="43",
                                midi_key=71,
                                midi_notes=[
                                    MidiNote(
                                        time=0.6666666666666666,
                                        duration=0.3333333333333333,
                                        velocity=90,
                                        midi_key=71,
                                    ),
                                    MidiNote(
                                        time=2.6666666666666665,
                                        duration=0.3333333333333333,
                                        velocity=90,
                                        midi_key=71,
                                    ),
                                ],
                            ),
                            KeyTrack(
                                id="44",
                                midi_key=72,
                                midi_notes=[
                                    MidiNote(
                                        time=2.3333333333333335,
                                        duration=0.3333333333333333,
                                        velocity=90,
                                        midi_key=72,
                                    ),
                                    MidiNote(
                                        time=3.6666666666666665,
                                        duration=0.3333333333333333,
                                        velocity=90,
                                        midi_key=72,
                                    ),
                                ],
                            ),
                            KeyTrack(
                                id="45",
                                midi_key=73,
                                midi_notes=[
                                    MidiNote(
                                        time=1.0,
                                        duration=0.3333333333333333,
                                        velocity=90,
                                        midi_key=73,
                                    )
                                ],
                            ),
                            KeyTrack(
                                id="46",
                                midi_key=74,
                                midi_notes=[
                                    MidiNote(
                                        time=1.3333333333333333,
                                        duration=0.3333333333333333,
                                        velocity=90,
                                        midi_key=74,
                                    ),
                                    MidiNote(
                                        time=3.3333333333333335,
                                        duration=0.3333333333333333,
                                        velocity=90,
                                        midi_key=74,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            MidiTrack(name="With Shift", has_drum_rack=False, drum_ruck_branches=[], midi_clips=[]),
        ],
        audio_tracks=[],
    )
