import os
import music21

def analyze_music_corpus(corpus_directory):
    """
    Analyze a music corpus by parsing all files in the specified directory,
    extracting the metadata, and calculating relevant statistics.

    Args:
    corpus_directory (str): path to the directory containing the music files

    Returns:
    analysis (dict): a dictionary containing metadata and statistics for the music corpus
    """

    # Initialize analysis dictionary
    analysis = {
        "file_count": 0,
        "composers": {},
        "key_signatures": {},
        "time_signatures": {},
        "average_notes_per_measure": 0,
    }

    # Initialize note counter and measure counter
    note_counter = 0
    measure_counter = 0

    # Iterate over all files in the corpus directory
    for root, _, filenames in os.walk(corpus_directory):
        for filename in filenames:

            # Check for valid music file extensions
            if filename.lower().endswith(('.mxl', '.xml', '.midi', '.mid')):
                file_path = os.path.join(root, filename)

                # Parse music file
                try:
                    music_piece = music21.converter.parse(file_path)
                except Exception as e:
                    print(f"Error parsing {file_path}: {e}")
                    continue

                # Extract metadata
                composer = music_piece.metadata.composer
                key_signature = music_piece.analyze("key")
                time_signature = music_piece.getTimeSignatures()[0]

                # Update composer count
                if composer in analysis["composers"]:
                    analysis["composers"][composer] += 1
                else:
                    analysis["composers"][composer] = 1

                # Update key signature count
                if key_signature in analysis["key_signatures"]:
                    analysis["key_signatures"][key_signature] += 1
                else:
                    analysis["key_signatures"][key_signature] = 1

                # Update time signature count
                if time_signature in analysis["time_signatures"]:
                    analysis["time_signatures"][time_signature] += 1
                else:
                    analysis["time_signatures"][time_signature] = 1

                # Count notes and measures
                for part in music_piece.parts:
                    for measure in part.getElementsByClass("Measure"):
                        note_counter += len(measure.notes)
                        measure_counter += 1

                # Increment file count
                analysis["file_count"] += 1

    # Calculate average notes per measure
    if measure_counter > 0:
        analysis["average_notes_per_measure"] = note_counter / measure_counter

    return analysis