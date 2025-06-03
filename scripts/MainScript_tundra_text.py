# -*- coding: utf-8 -*-

import sys, os

import audio2face_pb2
import audio2face_pb2_grpc

import grpc
from audio2face_streaming_utils import push_audio_track

import soundfile

import requests
import time
import numpy as np
import threading

from TTS.api import TTS

# from styletts2 import tts

from pysentimiento import create_analyzer

import openai

import pythonosc
from pythonosc import udp_client

import re
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu|me)"
digits = "([0-9])"
multiple_dots = r'\.{2,}'

import warnings
warnings.filterwarnings("ignore")

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def split_into_sentences(text: str) -> list[str]:
    """
    Split the text into sentences.

    If the text contains substrings "<prd>" or "<stop>", they would lead 
    to incorrect splitting because they are used as markers for splitting.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    text = re.sub("[*]", "<stop>", text)
    text = re.sub("([0-9]+)" + "[.]", "<stop>\\1<prd>", text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace(":",":<stop>")
    text = text.replace(";",";<stop>")
    text = text.replace(" - ", " - <stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]: sentences = sentences[:-1]
    return sentences
# # set USD and A2F instance
# def A2F():
# 	global a2f_instance
# 	payload = {
# 		"file_name": usd_scene
# 		}

# 	usd = requests.post(f'{server}/A2F/USD/Load', json=payload)

# 	print(f"USD scene: {usd.json()['message']}")

# 	a2f_instance = requests.get(f'{server}/A2F/GetInstances').json()
# 	a2f_instance = a2f_instance['result']['fullface_instances'][0]
# 	print(f'A2F Instance: {a2f_instance}')
# 	return a2f_instance

# # Emotion set
# def A2E():
# 	payload = {
# 	  "a2f_instance": a2f_instance,
# 	  "emotions": {
# 	    "neutral": 0,
# 	    "amazement": emo.probas['surprise'],
# 	    "anger": emo.probas['anger'],
# 	    "cheekiness": 0,
# 	    "disgust": emo.probas['disgust'],
# 	    "fear": emo.probas['fear'],
# 	    "grief": 0,
# 	    "joy": emo.probas['joy'],
# 	    "outofbreath": 0,
# 	    "pain": 0,
# 	    "sadness": emo.probas['sadness']
# 			}
# 		}

# 	a2e = requests.post(f'{server}/A2F/A2E/SetEmotionByName', json=payload)
# 	print(f'A2E parameters: {a2e.json()["message"]}')


# a2f_url = 'localhost:50051' # The audio2face url by default
# sample_rate = 22050 # Audio frame rate
# a2f_avatar_instance = '/World/audio2face/PlayerStreaming' # The instance name of the avatar in a2f
# #audio_fpath = 'F:/AI/Coqui/1674760854.wav'

# server = 'http://localhost:8011'
# usd_scene = 'C:/Users/Kyra/AppData/Local/ov/pkg/audio2face-2022.2.1/exts/omni.audio2face.wizard/assets/demo_fullface_streaming.usd'
# #audio_path = 'F:/A2F/!script/input_audio'

# tts = TTS(model_name="tts_models/en/multi-dataset/tortoise-v2", progress_bar=False, gpu=True)

# tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=True)
# tts = tts.StyleTTS2()

# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

# emotion_analyzer = create_analyzer(task="emotion", lang="en")

blockPrint()

openai.api_base = "http://localhost:1234/v1"
openai.api_key = "lm-studio"

# a2f_instance = A2F()

# client = udp_client.SimpleUDPClient('127.0.0.1', 5008)
# client.send_message("/FaceIdle", float(0))

assistant_text = "Hello."

stop_token = [".", "!", "?", ":", ";"]
stop_digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
# hmm = tts.tts(text="Hurm.", speaker=tts.speakers[30])
# hmmarr = np.array(hmm, dtype=np.float32)

start_time = time.time()

messages = [{
				"role": "system",
				"content": "You are currently participating in the Tundra Survival Problem with the user. The scenario is that your plane has crashed in the woods of northern Minnesota in the winter. You and the user must rank the importance of 15 items in order to survive. The items are as follows: a compress kit with gauze, a cigarette lighter without the fluid, a newspaper per person, two ski poles, a map of the area, a chocolate bar per person, a quart of whiskey, a can of shortening, a ball of steel wool, a loaded pistol, a magnetic compass, a knife, 30 feet of rope, a flashlight with batteries, and shirt and pants for each person. You are a middle aged white American male with no expert knowledge in survival matters, but are fairly confident in your intuition. The user will have to be quite convincing to change your mind. Reply as though you are speaking casually."
			}]

with open('tundra_text_experiment_log.csv', 'w') as f:
	while True:

		enablePrint()
		text_in = input('Enter text (Do not CTRL+C, only use left and right arrows and backspace): ')

		f.write(f'{time.time() - start_time}, "{text_in}", user\n')

		if text_in == '!exit':
			break

		if len(text_in) > 0:

			# push_audio_track(a2f_url, hmmarr, sample_rate, a2f_avatar_instance)

			# text = text_in
			blockPrint()
			messages.append({"role": "user", "content": text_in})
			completion = openai.ChatCompletion.create(
				model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
				messages=messages
					,temperature=0.7, stream=True)

			# text = completion.choices[0].message.content
			# assistant_text = text

			# # emo = emotion_analyzer.predict(text)
			# # print(f'Emotion: {emo.output}')
			# #threading.Thread(target=A2E).start()

			# # A2E()

			# print(text)

			# # Run TTS
			# wav = tts.tts(text=text, speaker=tts.speakers[30])
			# wavarr = np.array(wav, dtype=np.float32)

			# # client.send_message("/FaceIdle", float(1))
			# push_audio_track(a2f_url, wavarr, sample_rate, a2f_avatar_instance)
			# client.send_message("/FaceIdle", float(0))

			assistant_text = ""
			sentence_count = 0

			for chunk in completion:
				if chunk.choices[0].finish_reason != "stop":
					assistant_text += chunk.choices[0].delta.content
					text_list = split_into_sentences(assistant_text)
					text_list = [x for x in text_list if x]
					if len(text_list) > sentence_count + 1:
						text = text_list[-2]
						sentence_count += 1
						f.write(f'{time.time() - start_time}, "{text}", agent\n')
						enablePrint()
						print(text)
						blockPrint()
						# wav = tts.tts(text=text, speaker=tts.speakers[30], speed=0.3, )
						# wav = tts.tts(text=text,
						# 	speaker="Andrew Chipper",
						# 	language="en")
						# wavarr = np.array(wav, dtype=np.float32)
						# push_audio_track(a2f_url, wavarr, sample_rate, a2f_avatar_instance)
			text_list = split_into_sentences(assistant_text)
			text_list = [x for x in text_list if x]
			text = text_list[-1]
			f.write(f'{time.time() - start_time}, "{text}", agent\n')
			enablePrint()
			print(text)
			blockPrint()
			messages.append({"role": "assistant", "content": assistant_text})

#  and assistant_text[-2] not in stop_digits