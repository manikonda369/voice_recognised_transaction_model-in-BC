import speech_recognition as sr
import pyttsx3
import pveagle
import pvrecorder as pv
import time

DEFAULT_DEVICE_INDEX = -1
access_key = "oQCnEjICVIX3j8cTnHSM1Kw4Nq8r0ksaOlTFzriWgnWCwZGOJzrZ9g=="

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'male' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()

def recognize_speakers(speaker_profiles):
    try:
        eagle_recognizer = pveagle.create_recognizer(
            access_key=access_key,
            speaker_profiles=[profile for _, profile in speaker_profiles])
    except pveagle.EagleError as e:
        print(f"Error creating recognizer: {e}")
        return

    recognizer_recorder = pv.PvRecorder(
        device_index=DEFAULT_DEVICE_INDEX,
        frame_length=eagle_recognizer.frame_length)

    print("Recognition Starts")
    start_time = time.time()
    recognizer_recorder.start()

    end_time = time.time() + 5
    audio_frames = []
    while time.time() < end_time:
        audio_frame = recognizer_recorder.read()
        audio_frames.append(audio_frame)

    recognizer_recorder.stop()
    stop_time = time.time() 
    print(f"Recognition Ends. Recording duration: {stop_time - start_time:.2f} seconds")

    recognized_speaker_name = None 

    for frame in audio_frames:
        scores = eagle_recognizer.process(frame)
        if scores:
            max_score_index = scores.index(max(scores))
            if scores[max_score_index] > 0.5: 
                recognized_speaker_name = speaker_profiles[max_score_index][0]  
                break  

    recognizer_recorder.delete()
    eagle_recognizer.delete()
    if recognized_speaker_name:
        print(f"Recognized: {recognized_speaker_name}")
        speak(f"Recognized: {recognized_speaker_name}")
        return True, recognized_speaker_name
    else:
        print("User not found")
        speak("User not found")
        return False, None