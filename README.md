# Speech Segmentation from Audio 🎙️✂️

A Python script to automatically detect speech in an audio or video file, segment it into individual clips, and export the corresponding timestamps.

This tool is useful for pre-processing audio for transcription, creating datasets for voice analysis, or simply breaking down long recordings into manageable parts.

---

## Features

✅ **Video to Audio**: Extracts the audio track from any common video format (e.g., MP4, MOV).
✅ **Audio Standardization**: Converts audio to a standard format (16 kHz, mono WAV) for consistent processing.
✅ **Speech Detection**: Intelligently identifies segments of speech by detecting periods of silence.
✅ **Segment Export**: Saves each continuous speech segment as a separate `.wav` file.
✅ **Timestamp Generation**: Creates a `.json` file containing the precise `start` and `end` timestamps for every speech clip.

---

## File Structure

```
.
├── .gitignore
├── README.md
├── requirements.txt
├── segment_speech.py
├── input/
│   └── downloaded_video.mp4
└── output/
    ├── extracted_audio.wav
    ├── speech_timestamps.json
    └── segmented_clips/
        ├── segment_01.wav
        └── segment_02.wav
```

---

## 🛠️ Installation & Setup

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository

```bash
git clone [https://github.com/raghavxi1/speech-segmentation-project.git](https://github.com/raghavxi1/speech-segmentation-project.git)
cd speech-segmentation-project
```

### 2. Install FFmpeg

The `pydub` library requires **FFmpeg** to be installed on your system.

* **Windows**: Download from the [FFmpeg website](https://ffmpeg.org/download.html) and add the `bin` folder to your system's PATH.
* **macOS (via Homebrew)**: `brew install ffmpeg`
* **Linux (via apt)**: `sudo apt-get install ffmpeg`

### 3. Install Python Dependencies

It's recommended to use a virtual environment.

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install the required packages
pip install -r requirements.txt
```

---

## 🚀 How to Use

1.  **Add Your File**: Place your video or audio file ( `my_video.mp4`) inside the `input/` directory.

2.  **Update Script**: Open `segment_speech.py` and change the `INPUT_FILE` variable to point to your file:
    ```python
    # In segment_speech.py
    INPUT_FILE = "input/my_video.mp4" 
    ```

3.  **Run the Script**: Execute the script from your terminal:
    ```bash
    python segment_speech.py
    ```

4.  **Check the Output**: Once the script is finished, the `output/` directory will be populated with:
    * `extracted_audio.wav`: The full, standardized audio track.
    * `speech_timestamps.json`: A JSON file with all detected speech timestamps.
    * `segmented_clips/`: A folder containing all the exported `.wav` speech clips.

---

## ⚙️ Configuration

You can fine-tune the speech detection by adjusting the parameters at the top of the `segment_speech.py` script.

| Parameter             | Description                                                                                             | Default Value |
| --------------------- | ------------------------------------------------------------------------------------------------------- | ------------- |
| `SILENCE_THRESH_DBFS` | The volume threshold (in dBFS). Anything quieter than this is considered silence. Lower it for noisy audio. | `-40.0`       |
| `MIN_SILENCE_LEN_MS`  | The minimum duration (in ms) of a silent pause between speech segments.                                   | `500`         |
| `MIN_SPEECH_LEN_MS`   | The minimum duration (in ms) for a sound to be considered a speech segment. Prevents saving short noises.   | `250`         |
| `PADDING_MS`          | Adds a bit of silence (in ms) to the beginning and end of each clip to avoid cutting off words.           | `150`         |

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.