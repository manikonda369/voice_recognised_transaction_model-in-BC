import speech_recognition as sr
import pyttsx3
#import multiprocessing as mp
from enroll_speaker import enroll_speaker
from recognise_speaker import recognize_speakers
from web3 import Web3
import json
# import time
global count


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))


with open('build/contracts/SimpleBank.json') as f:
    abi = json.load(f)['abi']

contract = w3.eth.contract(address="0x893EA8D4910CFB256f867B9aFfF38FdFd864E71D", abi=abi)

w3.eth.default_account = w3.eth.accounts[0]
owner=contract.functions.getOwner().call()


def speak(*texts):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'male' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    for text in texts:
        engine.say(text)
    engine.runAndWait()


def listen_for_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for commands...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print(f"Received command: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return None
    except sr.RequestError as e:
        speak(f"Sorry, I couldn't request results from the service; {e}")
        return None



def voice_assistant():
    speak("Welcome. Say 'enroll' to start the enrollment.")
    command = listen_for_command()
    if command and "enroll" in command:
        speak("Starting enrollment.")
        speak("Please state your name for enrollment.")
        user_name = listen_for_command()  # Capture the user's name
        if user_name:

            speaker_profiles = enroll_speaker(user_name) 
             # Enroll the user with their name
            if speaker_profiles:
                speak("Enrollment completed successfully. Now, let's verify your voice.")
                count=0
                tx_hash = contract.functions.enroll(w3.eth.accounts[count],user_name).transact({'from' : owner})
                count=count+1
                receipt=w3.eth.wait_for_transaction_receipt(tx_hash)
                print(receipt)
                print("Account Created Successfully With Address: ",w3.eth.accounts[0])
                speak("Account Created Successfully With Address: ",w3.eth.accounts[0])

                # Attempt to verify the speaker
                verified, speaker_name = recognize_speakers(speaker_profiles)
                if verified:
                    speak(f"Voice verified successfully, {speaker_name}. You can now use the services.")
                    # Enter a loop for using the services

                    while True:
                        command = listen_for_command()
                        if command:

                            # exitting
                            if "exit" in command:
                                speak("Exiting. Goodbye!")
                                break

                            #time
                            elif "time" in command:
                                from datetime import datetime
                                now = datetime.now()
                                current_time = now.strftime("%H:%M")
                                speak(f"The current time is {current_time}.")

                            # Enrollment of contact
                            elif "enroll" in command:
                                speak("Please state Contact name for enrollment.")
                                name = input("Enter The Name : ")
                                if contract.functions.isEnrolled(name).call():
                                    speak("User Already Enrolled")
                                else:
                                    speak("Enter The Address of the contact")
                                    address = w3.eth.accounts[count]  # Use the count as the index to get the account address

                                    tx_hash = contract.functions.enroll(address,name).transact({'from': owner})
                                    speak(f"Request sent :{tx_hash.hex()}")
                                    print(f"Request sent :{tx_hash.hex()}")
                                    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                                    speak(f"Request confirmed in block: {receipt.blockNumber}")
                                    print(f"Request confirmed in block: {receipt.blockNumber}")

                                    print("Contact Enrolled Successfully")
                                    speak("Contact Enrolled Successfully")

                                    # Increment the count
                                    count += 1

                            # Delete Contact
                            elif "unenroll" in command:
                                speak("Please state the name of the contact to unenroll.")
                                name=listen_for_command()
                                if(contract.functions.isEnrolled(name).call()):
                                    tx_hash = contract.functions.unenroll(name).transact()
                                    speak(f"Request sent :{tx_hash.hex()}")
                                    print(f"Request sent :{tx_hash.hex()}")
                                    receipt=w3.eth.wait_for_transaction_receipt(tx_hash)
                                    speak(f"Request confirmed in block: {receipt.blockNumber}")
                                    print(f"Request confirmed in block: {receipt.blockNumber}")

                                    print("Contact Unenrolled Successfully")
                                    speak("Contact Unenrolled Successfully")
                                else:
                                    print("Contact Not Enrolled")
                                    speak("Contact Not Enrolled")

                            # isEnrolled
                            elif "is enroll" in command:
                                speak("Please state the name of the contact to check.")
                                name=listen_for_command()
                                if(contract.functions.isEnrolled(name).call()):
                                    print("Contact Enrolled")
                                    speak("Contact Enrolled")
                                else:
                                    print("Contact Not Enrolled")
                                    speak("Contact Not Enrolled")

                            # getAddress
                            elif "get address" in command:
                                speak("Please state the name of the contact to get address.")
                                name=listen_for_command()
                                if(contract.functions.isEnrolled(name).call()):
                                    address=contract.functions.getAddress(name).call()
                                    print(f"Address of {name} is {address}")
                                    speak(f"Address of {name} is {address}")
                                else:
                                    print("Contact Not Enrolled")
                                    speak("Contact Not Enrolled")

                            # Balance
                            elif "balance" in command:
                                balance=contract.functions.balanceOf().call()
                                print("Current Balance In Your Account Is : ",balance)
                                speak("Current Balance In Your Account Is : ",balance)
                            
                            # Transfer
                            elif "transfer" in command:
                                speak("Please Enter The Name of the Person to Transfer Amount")
                                name=listen_for_command()
                                if(contract.functions.isEnrolled(name).call()):
                                    speak("Please State The Amount To Transfer")
                                    amount=int(input("Enter The Amount"))
                                    if(amount <= contract.functions.balanceOf().call()):
                                        tx_hash = contract.functions.transfer(name,amount).transact()
                                        speak(f"Request sent :{tx_hash.hex()}")
                                        print(f"Request sent :{tx_hash.hex()}")
                                        receipt=w3.eth.wait_for_transaction_receipt(tx_hash)
                                        speak(f"Request confirmed in block: {receipt.blockNumber}")
                                        print(f"Request confirmed in block: {receipt.blockNumber}")
                                    else:
                                        speak("Amount Not Sufficient")
                                        print("Amount Not Sufficient")
                                else:
                                    print("User Not Enrolled")
                                    speak("User Not Enrolled")
                            
                            # Deposit
                            elif "deposit" in command:
                                speak("Enter The Amount To Be Deposited")
                                amount=int(input("Enter The Amount To Be Deposited : "))
                                tx_hash = contract.functions.deposit(amount).transact()
                                print(f"Request sent: {tx_hash.hex()}")
                                speak(f"Request sent: {tx_hash.hex()}")
                                receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                                print(f"Request confirmed in block: {receipt.blockNumber}")
                                speak(f"Request confirmed in block: {receipt.blockNumber}")


                            else:
                                speak("Sorry, I didn't understand that command. You can say 'time' or 'exit'.")
                else:
                    speak("Speaker recognition failed. Please try enrolling again.")
            else:
                speak("Enrollment failed. Please try again.")
        else:
            speak("Name not captured. Please try enrolling again.")
    else:
        speak("No enrollment command detected. Exiting.")

if __name__ == "__main__":
    voice_assistant()