import random

def music_playlist_generator(songs, num_of_songs=10):
  """
  This function generates a music playlist with a given number of songs from a list of available songs.

  :param songs: A list of available songs.
  :type songs: list of str
  
  :param num_of_songs: The number of songs desired in the playlist. Default value is 10.
  :type num_of_songs: int
  
  :return: A generated playlist with specified number of songs randomly selected from the input list.
  :rtype: list of str
  """

  if not isinstance(songs, list) or not all(isinstance(song, str) for song in songs):
    raise ValueError("songs must be a list of strings")

  if not isinstance(num_of_songs, int) or num_of_songs < 1:
    raise ValueError("num_of_songs must be a positive integer")

  if num_of_songs > len(songs):
    raise ValueError(f"num_of_songs({num_of_songs}) cannot be greater than the number of available songs({len(songs)})")

  shuffled_songs = random.sample(songs, len(songs))
  return shuffled_songs[:num_of_songs]


# Example usage
available_songs = [
  "Song 1",
  "Song 2",
  "Song 3",
  "Song 4",
  "Song 5",
  "Song 6",
  "Song 7",
  "Song 8",
  "Song 9",
  "Song 10",
  "Song 11",
  "Song 12",
]

playlist = music_playlist_generator(available_songs, 5)
print("Generated Playlist:", playlist)