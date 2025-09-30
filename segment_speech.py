import os
import json
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.silence import detect_silence

# --- 1. CONFIGURATION ---

# NOTE: Place your video file in the 'input' directory and update this name.
INPUT_FILE_NAME = "downloaded_video.mp4" 

# Output directories and file paths
INPUT_DIR = "input"
OUTPUT_DIR = "output"
SEGMENT_DIR = os.path.join(OUTPUT_DIR, "segmented_clips")
EXTRACTED_AUDIO_PATH = os.path.join(OUTPUT_DIR, "extracted_audio.wav")
TIMESTAMPS_PATH = os.path.join(OUTPUT_DIR, "speech_timestamps.json")

# Audio standardization parameters
SAMPLE_RATE = 16000
CHANNELS = 1 # Mono

# Speech detection parameters (tweak these for your specific audio)
SILENCE_THRESH_DBFS = -40.0  # The upper bound for how loud a sound can be to be considered silence.
MIN_SILENCE_LEN_MS = 500     # Minimum length of a silence chunk in milliseconds.
MIN_SPEECH_LEN_MS = 250      # Minimum length of a speech segment to be saved.
PADDING_MS = 150             # Add padding to the start/end of each clip to avoid cutting off words.


def setup_directories():
    """Create the necessary input and output directories."""
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(SEGMENT_DIR, exist_ok=True)


def extract_and_standardize_audio(video_path):
    """
    Task 1: Extracts audio from a video file, saves it, and standardizes it.
    - Converts to WAV format.
    - Sets to mono channel.
    - Sets to a 16 kHz sample rate.
    """
    if not os.path.exists(video_path):
        print(f"❌ ERROR: Input file not found at '{video_path}'")
        print("Please place your video file in the 'input' directory and check the INPUT_FILE_NAME.")
        return None

    print(f"1. Extracting and standardizing audio from '{video_path}'...")
    
    try:
        # Extract audio using moviepy
        video_clip = VideoFileClip(video_path)
        video_clip.audio.write_audiofile(EXTRACTED_AUDIO_PATH, codec='pcm_s16le')
        video_clip.close()
        
        # Load with pydub and standardize
        audio = AudioSegment.from_wav(EXTRACTED_AUDIO_PATH)
        audio = audio.set_frame_rate(SAMPLE_RATE)
        audio = audio.set_channels(CHANNELS)
        audio.export(EXTRACTED_AUDIO_PATH, format="wav") # Overwrite with standardized version
        
        print("   ✅ Audio extracted and standardized successfully.")
        return audio
    except Exception as e:
        print(f"   ❌ An error occurred during audio extraction: {e}")
        return None


def detect_speech_timestamps(audio):
    """
    Task 2: Analyzes audio to find speech segments based on silence.
    Returns a list of dictionaries with 'start' and 'end' timestamps in seconds.
    """
    print("2. Detecting speech segments...")
    
    # Use pydub's silence detection to find ranges of SILENCE.
    silent_ranges = detect_silence(
        audio,
        min_silence_len=MIN_SILENCE_LEN_MS,
        silence_thresh=SILENCE_THRESH_DBFS
    )

    # Invert silent ranges to get speech ranges.
    speech_timestamps = []
    last_end = 0
    audio_len_ms = len(audio)

    for start_silence, end_silence in silent_ranges:
        speech_start = last_end
        speech_end = start_silence
        
        if speech_end - speech_start > MIN_SPEECH_LEN_MS:
            speech_timestamps.append([speech_start, speech_end])
        
        last_end = end_silence
        
    # Check for speech after the last silence detected
    if audio_len_ms - last_end > MIN_SPEECH_LEN_MS:
        speech_timestamps.append([last_end, audio_len_ms])

    if not speech_timestamps:
        print("   ⚠️ No speech detected.")
        return []

    # Format timestamps into a list of dictionaries (in seconds)
    formatted_timestamps = [
        {"start": start / 1000.0, "end": end / 1000.0}
        for start, end in speech_timestamps
    ]

    # Save timestamps to a JSON file
    with open(TIMESTAMPS_PATH, 'w') as f:
        json.dump(formatted_timestamps, f, indent=2)
        
    print(f"   ✅ Detected {len(formatted_timestamps)} speech segments. Timestamps saved to '{TIMESTAMPS_PATH}'.")
    return formatted_timestamps


def segment_and_export_clips(audio, timestamps):
    """
    Task 3: Splits the audio into smaller clips based on timestamps and exports them.
    """
    if not timestamps:
        print("   ⏩ No timestamps provided, skipping segmentation.")
        return

    print("3. Segmenting and exporting audio clips...")
    
    for i, ts in enumerate(timestamps):
        start_ms = int(ts['start'] * 1000)
        end_ms = int(ts['end'] * 1000)

        # Apply padding, ensuring we don't go out of the audio's bounds
        padded_start = max(0, start_ms - PADDING_MS)
        padded_end = min(len(audio), end_ms + PADDING_MS)

        # Extract the segment
        segment = audio[padded_start:padded_end]
        
        # Define output filename (e.g., segment_01.wav)
        filename = f"segment_{i+1:02d}.wav"
        output_path = os.path.join(SEGMENT_DIR, filename)
        
        # Export the segment
        segment.export(output_path, format="wav")
    
    print(f"   ✅ Successfully exported {len(timestamps)} clips to '{SEGMENT_DIR}'.")


def main():
    """Main function to run the entire speech segmentation pipeline."""
    setup_directories()
    
    input_path = os.path.join(INPUT_DIR, INPUT_FILE_NAME)

    # --- Run the pipeline ---
    standardized_audio = extract_and_standardize_audio(input_path)
    
    if standardized_audio:
        speech_timestamps = detect_speech_timestamps(standardized_audio)
        segment_and_export_clips(standardized_audio, speech_timestamps)
        print("\n🎉 Assignment completed successfully!")

if __name__ == "__main__":
    main()