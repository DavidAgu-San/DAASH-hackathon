import time
from openai import OpenAI
import speech_recognition as sr
import pyttsx3

client = OpenAI(api_key = "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")

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(" Speak now")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)


        try:
            return recognizer.recognize_google(audio, show_all=False)
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Error: Speech service unavailable."

def Masterbot(prompt):

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a supportive and empathetic wellness assistant. Your goal is to provide moral support, listen actively, and offer helpful advice. Avoid stating that you are an AI or that you cannot feel emotions. Instead, focus on being understanding and human-like. "},
            {"role": "user", "content": prompt}]# would be trained with API's
    )
    return response.choices[0].message.content.strip()
def main():
    print("Masterbot: Hello! what can I help you with today?")
    text_to_speech("Hello! what can I help you with today?")
    choices = ["prescription", "symptoms", "side effects", "medication"]
    exit_phrases = ["quit", "end", "bye", "goodbye", "im fine", "I am safisfied with my care"]
    catious_phrases = ["I scared", "I am afraid", "Im not feeling well", "harm", "hurt", "anxious", "depressed"]
    while True:
        user_input = speech_to_text()
        print(f"You: {user_input}")

        if any(exit_phrase in user_input.lower() for exit_phrase in exit_phrases):
            text_to_speech("Take care! Remember to prioritize your well-being.")
            break
        if any(choice in user_input.lower() for choice in choices):
          text_to_speech("To assist you further, I need to verify your identity. Please scan your badge.")
          text_to_speech("Please wait while I verify your identity.")
          time.sleep(3)  # simulate a verification process
          text_to_speech("Identity verified. How are you feeling today?")
          continue
        if any(catious_phrase in user_input.lower() for catious_phrase in catious_phrases):
                text_to_speech("redirecting you to a live support agent") # would be linked a direct call to a live agent or 24/7 mental health platform(Timely)
                break

        response = Masterbot(user_input)
        print("MasterBot:", response)
        text_to_speech(response)

if __name__ == "__main__":
    main()