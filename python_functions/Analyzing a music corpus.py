def analyze_music_corpus(corpus):
    from collections import defaultdict, Counter
    
    note_counters = Counter()
    total_duration = 0
    pitch_frequency = defaultdict(int)
    pitch_duration = defaultdict(float)
    
    for note in corpus:
        pitch = note['pitch']
        duration = note['duration']
        start_time = note['start_time']
        
        total_duration += duration
        pitch_frequency[pitch] += 1
        pitch_duration[pitch] += duration
    
    average_duration = total_duration / len(corpus)
    most_common_pitches = note_counters.most_common(3)
    
    print(f"Total duration: {total_duration}")
    print(f"Average duration: {average_duration}")
    print("Top 3 pitch occurrences:")
    for pitch, count in most_common_pitches:
        print(f"  {pitch}: {count} times")
    print("Duration per pitch:")
    for pitch, duration in pitch_duration.items():
        print(f"  {pitch}: {duration} seconds")
        
# Example usage
analyze_music_corpus(music_corpus)