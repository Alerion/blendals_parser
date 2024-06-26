from blendals_parser import live_set
from blendals_parser.live_set import AudioChannelPoint
from blendals_parser.song import Song, MidiTrack, Note, AudioTrack, Point, Locator


def live_set_to_song(liveset: live_set.LiveSet) -> Song:
    song = Song(
        name=liveset.name,
        bpm=liveset.bpm,
        time_signature_numerator=liveset.time_signature_numerator,
        time_signature_denominator=liveset.time_signature_denominator,
        length_in_bars=liveset.length_in_bars,
        locators=[],
        midi_tracks=[],
        audio_tracks=[]
    )

    for locator in liveset.locators:
        song.locators.append(Locator(
            id=locator.id,
            name=locator.name,
            time=locator.time,
        ))

    for midi_track in liveset.midi_tracks:
        # Generate notes for each midi key from all midi clips.
        tracks_notes = {}
        for midi_clip in midi_track.midi_clips:
            midi_clip_track_notes = get_track_notes_from_midi_clip(midi_clip)
            for midi_key, notes in midi_clip_track_notes.items():
                if midi_key not in tracks_notes:
                    tracks_notes[midi_key] = []
                tracks_notes[midi_key].extend(notes)

        # Generate unique notes sequence per midi track and midi key.
        for midi_key, notes in tracks_notes.items():
            track = MidiTrack(
                id=_get_midi_track_name(midi_track, midi_key),
                notes=notes,
            )
            song.midi_tracks.append(track)

    for audio_track in liveset.audio_tracks:
        left_channel_track, right_channel_track = get_points_from_audio_track(
            audio_track
        )
        song.audio_tracks.append(left_channel_track)
        song.audio_tracks.append(right_channel_track)

    return song


def _get_midi_track_name(midi_track: live_set.MidiTrack, midi_key) -> str:
    if not midi_track.has_drum_rack:
        return f"{midi_track.name}:{midi_key}"

    branch_name = midi_key
    for branch in midi_track.drum_ruck_branches:
        if branch.midi_key == midi_key:
            branch_name = branch.name
            break

    return f"{midi_track.name}:{branch_name}"


def get_track_notes_from_midi_clip(
    midi_clip: live_set.MidiClip,
) -> dict[int, list[Note]]:
    tracks_notes = {}
    for key_track in midi_clip.key_tracks:
        notes = get_notes_from_key_track(
            midi_clip.start, midi_clip.end, key_track, midi_clip.loop
        )
        tracks_notes[key_track.midi_key] = notes
    return tracks_notes


def get_notes_from_key_track(
    start: float, end: float, key_track: live_set.KeyTrack, loop: live_set.Loop
) -> list[Note]:
    """
    If loop is enabled its length is equal to the length of the key_track.
    So midi_notes_in_loop contains only notes that are in the loop.
    And loops_count is equal to 1.
    """
    # In Ableton Live you can create a long key track and add only part of it into the midi track.
    # Get midi notes that are in the loop. Other midi notes are not used in the midi track.
    midi_notes_in_loop = []
    for midi_note in key_track.midi_notes:
        if loop.start <= midi_note.time <= loop.end:
            midi_notes_in_loop.append(midi_note)

    loop_length = loop.end - loop.start
    track_length = end - start
    notes = []

    # You can loop a key track and resize it into any length inside the midi clip.
    # So we generate notes for each loop.
    loops_count = int(track_length // loop_length)
    for i in range(loops_count):
        start_offset = start + i * loop_length
        for midi_note in midi_notes_in_loop:
            note_start = start_offset + midi_note.time
            node_end = note_start + midi_note.duration
            notes.append(
                Note(
                    start=note_start,
                    end=node_end,
                    velocity=midi_note.velocity,
                    midi_key=key_track.midi_key,
                )
            )

    # You resize a ket track to any length inside the midi clip.
    # So the last loop can be shorter than the others.
    start_offset = start + loops_count * loop_length
    last_loop_length = track_length % loop_length
    for midi_note in midi_notes_in_loop:
        if midi_note.time >= (loop.start + last_loop_length):
            break
        note_start = start_offset + midi_note.time
        node_end = note_start + midi_note.duration
        notes.append(
            Note(
                start=note_start,
                end=node_end,
                velocity=midi_note.velocity,
                midi_key=key_track.midi_key,
            )
        )

    return notes


def get_points_from_audio_track(
    audio_track: live_set.AudioTrack,
) -> tuple[AudioTrack, AudioTrack]:
    left_channel_points = []
    right_channel_points = []
    for audio_clip in audio_track.audio_clips:
        left_channel_points.extend(
            get_points_from_audio_channel_points(
                audio_clip.start,
                audio_clip.end,
                audio_clip.left_channel_points,
                audio_clip.loop,
            )
        )
        right_channel_points.extend(
            get_points_from_audio_channel_points(
                audio_clip.start,
                audio_clip.end,
                audio_clip.right_channel_points,
                audio_clip.loop,
            )
        )
    left_channel_track = AudioTrack(
        id=f"{audio_track.name}:left_channel",
        points=left_channel_points,
    )
    right_channel_track = AudioTrack(
        id=f"{audio_track.name}:right_channel",
        points=right_channel_points,
    )
    return left_channel_track, right_channel_track


def get_points_from_audio_channel_points(
    start: float,
    end: float,
    audio_channel_points: list[AudioChannelPoint],
    loop: live_set.Loop,
) -> list[Point]:
    """
    See get_notes_from_key_track for details.
    """
    audio_points_in_loop = []
    for point in audio_channel_points:
        if loop.start <= point.time <= loop.end:
            audio_points_in_loop.append(point)

    loop_length = loop.end - loop.start
    track_length = end - start
    output_points = []

    # You can loop a sample and resize it into any length inside the midi clip.
    # So we generate notes for each loop.
    loops_count = int(track_length // loop_length)
    for i in range(loops_count):
        start_offset = start + i * loop_length
        for audio_point in audio_points_in_loop:
            output_points.append(
                Point(
                    time=start_offset + audio_point.time,
                    value=audio_point.value,
                )
            )

    # You resize a sample to any length inside the midi clip.
    # So the last loop can be shorter than the others.
    start_offset = start + loops_count * loop_length
    last_loop_length = track_length % loop_length
    for audio_point in audio_points_in_loop:
        if audio_point.time > (loop.start + last_loop_length):
            break
        output_points.append(
            Point(
                time=start_offset + audio_point.time,
                value=audio_point.value,
            )
        )

    return output_points
