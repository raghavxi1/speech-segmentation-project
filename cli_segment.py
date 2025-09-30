#!/usr/bin/env python3
"""
Enhanced Speech Segmentation Tool with CLI
"""
import argparse
import os
import sys
from segment_speech import *

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Segment speech from audio/video files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_segment.py input/video.mp4
  python cli_segment.py input/audio.wav --threshold -35 --min-speech 500
  python cli_segment.py input/video.mp4 --output custom_output/
        """
    )
    
    parser.add_argument(
        'input_file',
        help='Path to the input video or audio file'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='output',
        help='Output directory (default: output)'
    )
    
    parser.add_argument(
        '--threshold', '-t',
        type=float,
        default=-40.0,
        help='Silence threshold in dBFS (default: -40.0)'
    )
    
    parser.add_argument(
        '--min-silence',
        type=int,
        default=500,
        help='Minimum silence length in ms (default: 500)'
    )
    
    parser.add_argument(
        '--min-speech',
        type=int,
        default=250,
        help='Minimum speech length in ms (default: 250)'
    )
    
    parser.add_argument(
        '--padding',
        type=int,
        default=150,
        help='Padding around segments in ms (default: 150)'
    )
    
    parser.add_argument(
        '--format',
        choices=['wav', 'mp3', 'flac'],
        default='wav',
        help='Output audio format (default: wav)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"❌ Error: Input file '{args.input_file}' not found")
        sys.exit(1)
    
    # Update global configuration based on arguments
    global OUTPUT_DIR, SILENCE_THRESH_DBFS, MIN_SILENCE_LEN_MS, MIN_SPEECH_LEN_MS, PADDING_MS
    OUTPUT_DIR = args.output
    SILENCE_THRESH_DBFS = args.threshold
    MIN_SILENCE_LEN_MS = args.min_silence
    MIN_SPEECH_LEN_MS = args.min_speech
    PADDING_MS = args.padding
    
    if args.verbose:
        print(f"🎯 Configuration:")
        print(f"   Input: {args.input_file}")
        print(f"   Output: {args.output}")
        print(f"   Silence threshold: {args.threshold} dBFS")
        print(f"   Min silence: {args.min_silence} ms")
        print(f"   Min speech: {args.min_speech} ms")
        print(f"   Padding: {args.padding} ms")
        print(f"   Format: {args.format}")
        print()
    
    # Run the processing pipeline
    setup_directories()
    standardized_audio = extract_and_standardize_audio(args.input_file)
    
    if standardized_audio:
        speech_timestamps = detect_speech_timestamps(standardized_audio)
        segment_and_export_clips(standardized_audio, speech_timestamps)
        
        if args.verbose:
            print(f"\n📊 Results:")
            print(f"   Total segments: {len(speech_timestamps)}")
            print(f"   Output directory: {args.output}")
        
        print("\n🎉 Processing completed successfully!")
    else:
        print("❌ Processing failed")
        sys.exit(1)

if __name__ == "__main__":
    main()