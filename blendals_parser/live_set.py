from dataclasses import dataclass, field
from typing import Optional

from lxml.etree import _Element as Element


@dataclass
class LiveSet:
    name: str
    bpm: int
    time_signature_numerator: int
    time_signature_denominator: int
    length_in_bars: int
    midi_tracks: list["MidiTrack"]
    audio_tracks: list["AudioTrack"]
    _element: Optional[Element] = field(default=None, repr=False, compare=False)


@dataclass
class AudioTrack:
    name: str
    audio_clips: list["AudioClip"]
    _element: Optional[Element] = field(default=None, repr=False, compare=False)


@dataclass
class AudioClip:
    id: str
    name: str
    start: float
    end: float
    loop: "Loop"
    time_signature: "TimeSignature"
    left_channel_points: list["AudioChannelPoint"]
    right_channel_points: list["AudioChannelPoint"]
    _element: Optional[Element] = field(default=None, repr=False, compare=False)


@dataclass
class AudioChannelPoint:
    time: float
    value: float


@dataclass
class MidiTrack:
    name: str
    has_drum_rack: bool
    drum_ruck_branches: list["DrumRuckBranch"]
    midi_clips: list["MidiClip"]
    _element: Optional[Element] = field(default=None, repr=False, compare=False)


@dataclass
class DrumRuckBranch:
    name: str
    midi_key: int


@dataclass
class MidiClip:
    id: str
    start: float
    end: float
    loop: "Loop"
    time_signature: "TimeSignature"
    key_tracks: list["KeyTrack"]
    _element: Optional[Element] = field(default=None, repr=False, compare=False)


@dataclass
class Loop:
    start: float
    end: float
    enabled: bool
    _element: Optional[Element] = field(default=None, repr=False, compare=False)


@dataclass
class TimeSignature:
    numerator: int
    denominator: int
    _element: Optional[Element] = field(default=None, repr=False, compare=False)


@dataclass
class KeyTrack:
    id: str
    midi_key: int
    midi_notes: list["MidiNote"]
    _element: Optional[Element] = field(default=None, repr=False, compare=False)


@dataclass
class MidiNote:
    time: float
    duration: float
    velocity: int
    midi_key: int
    _element: Optional[Element] = field(default=None, repr=False, compare=False)
