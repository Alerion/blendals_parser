from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Song:
    name: str
    bpm: int
    time_signature_numerator: int
    time_signature_denominator: int
    length_in_bars: float
    # Dacite does not work with build in list that is supported from 3.9. So use List instead of list.
    locators: List[Locator]
    midi_tracks: List[MidiTrack]
    audio_tracks: List[AudioTrack]

    def get_midi_track(self, track_id: str) -> MidiTrack:
        for track in self.midi_tracks:
            if track.id == track_id:
                return track
        raise KeyError(track_id)


@dataclass
class Locator:
    id: str
    name: str
    time: float


@dataclass
class MidiTrack:
    id: str
    notes: list[Note]


@dataclass
class Note:
    start: float  # beats
    end: float  # beats
    velocity: int
    midi_key: int


@dataclass
class AudioTrack:
    id: str
    points: list[Point]


@dataclass
class Point:
    time: float
    value: float
