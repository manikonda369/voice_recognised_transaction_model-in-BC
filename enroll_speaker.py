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

def enroll_speaker(speaker_name):
    speaker_profiles = []
    try:
        eagle_profiler = pveagle.create_profiler(access_key=access_key)
    except pveagle.EagleError as e:
        print(f"Error creating profiler: {e}")
        return None
    enroll_recorder = pv.PvRecorder(
        device_index=DEFAULT_DEVICE_INDEX,
        frame_length=eagle_profiler.min_enroll_samples)

    enroll_recorder.start()
    print(f"Enrollment Starts for {speaker_name}")
    speak("Please start speaking now to enroll.")

    enroll_percentage = 0.0
    start_time = time.time()
    while enroll_percentage < 100.0 and time.time() - start_time < 50:
        audio_frame = enroll_recorder.read()
        enroll_percentage, feedback = eagle_profiler.enroll(audio_frame)
        print(f"Enrollment Progress for {speaker_name}: {enroll_percentage}% - Feedback: {feedback}")

    enroll_recorder.stop()

    print(f"Enrollment Ends for {speaker_name}")
    if enroll_percentage >= 100.0:
        speaker_profile = eagle_profiler.export()
        enroll_recorder.delete()
        eagle_profiler.delete()
        print(f"Enrollment for {speaker_name} is completed.")
        speaker_profiles.append((speaker_name, speaker_profile))
        return speaker_profiles
    else:
        print(f"Enrollment for {speaker_name} was not completed in time.")
        speak("Enrollment was not completed within time. Please try again.")
        return None