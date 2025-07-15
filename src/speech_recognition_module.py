#!/usr/bin/env python3
"""
Speech Recognition Module for Nova Carter3 Robot Control
Converts voice commands to text for ChatGPT processing
"""

import speech_recognition as sr
import pyaudio
import logging
from typing import Optional

class SpeechRecognitionModule:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.logger = logging.getLogger(__name__)
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            
    def listen_for_command(self, timeout: int = 10) -> Optional[str]:
        """
        Listen for voice command and convert to text
        
        Args:
            timeout: Maximum time to wait for speech
            
        Returns:
            Transcribed text or None if no speech detected
        """
        try:
            with self.microphone as source:
                self.logger.info("Listening for command...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
                
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            self.logger.info(f"Recognized: {text}")
            return text
            
        except sr.WaitTimeoutError:
            self.logger.warning("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            self.logger.error("Could not understand audio")
            return None
        except sr.RequestError as e:
            self.logger.error(f"Speech recognition service error: {e}")
            return None
            
    def continuous_listen(self, callback_function):
        """
        Continuously listen for voice commands
        
        Args:
            callback_function: Function to call with recognized text
        """
        while True:
            command = self.listen_for_command()
            if command:
                callback_function(command)