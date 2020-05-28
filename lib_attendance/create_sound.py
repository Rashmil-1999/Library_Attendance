from gtts import gTTS
import os


def generate_sound_file(text):
    """
        Receives a text input and generates a sound corresponding to the text
        Outputs a mp3 file corresponding to the input
    """
    filename = "_".join(text.strip().split(" "))
    myObj = gTTS(text=text, lang="en", slow=False)
    myObj.save("media/{}.mp3".format(filename))


if not os.path.exists("media"):
    os.mkdir("media")
generate_sound_file("Try again")
