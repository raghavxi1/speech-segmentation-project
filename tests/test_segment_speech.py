"""
Unit tests for speech segmentation functionality
"""
import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from segment_speech import setup_directories, detect_speech_timestamps

class TestSpeechSegmentation(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.original_input_dir = os.path.join(self.test_dir, "input")
        self.original_output_dir = os.path.join(self.test_dir, "output")
    
    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_setup_directories(self):
        """Test that directories are created correctly."""
        with patch('segment_speech.INPUT_DIR', self.original_input_dir):
            with patch('segment_speech.SEGMENT_DIR', os.path.join(self.original_output_dir, "segmented_clips")):
                setup_directories()
                
                self.assertTrue(os.path.exists(self.original_input_dir))
                self.assertTrue(os.path.exists(os.path.join(self.original_output_dir, "segmented_clips")))
    
    @patch('segment_speech.detect_silence')
    def test_detect_speech_timestamps_empty_audio(self, mock_detect_silence):
        """Test speech detection with no speech found."""
        # Mock audio object
        mock_audio = MagicMock()
        mock_audio.__len__ = MagicMock(return_value=10000)  # 10 seconds
        
        # Mock detect_silence to return silence covering the entire audio
        mock_detect_silence.return_value = [(0, 10000)]
        
        with patch('segment_speech.TIMESTAMPS_PATH', os.path.join(self.test_dir, "timestamps.json")):
            result = detect_speech_timestamps(mock_audio)
            
            self.assertEqual(len(result), 0)
    
    @patch('segment_speech.detect_silence')
    def test_detect_speech_timestamps_with_speech(self, mock_detect_silence):
        """Test speech detection with speech segments found."""
        # Mock audio object
        mock_audio = MagicMock()
        mock_audio.__len__ = MagicMock(return_value=10000)  # 10 seconds
        
        # Mock detect_silence to return some silent periods
        mock_detect_silence.return_value = [(2000, 3000), (6000, 7000)]
        
        with patch('segment_speech.TIMESTAMPS_PATH', os.path.join(self.test_dir, "timestamps.json")):
            with patch('segment_speech.MIN_SPEECH_LEN_MS', 500):
                result = detect_speech_timestamps(mock_audio)
                
                # Should detect speech at: 0-2000ms, 3000-6000ms, 7000-10000ms
                self.assertEqual(len(result), 3)
                self.assertEqual(result[0]['start'], 0.0)
                self.assertEqual(result[0]['end'], 2.0)
                self.assertEqual(result[1]['start'], 3.0)
                self.assertEqual(result[1]['end'], 6.0)

if __name__ == '__main__':
    unittest.main()