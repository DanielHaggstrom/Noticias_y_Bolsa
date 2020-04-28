# Dado una lista de textos, vamos a asociar un score según lo positivo o negativo que es
import math
import pandas as pd
import numpy as np
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

def get_score(text_list):
    sia = SIA()
    return [sia.polarity_scores(text= text) for text in text_list]

examples = ["Apple is considering letting users set third-party apps as the iPhone and iPad’s default web browsers and "
            "email clients, Bloomberg reports. The company is also reportedly working on allowing third-party music"
            " services like Spotify to run directly on its HomePod smart speaker, bypassing the need to stream them"
            " from an Apple device over AirPlay. Although the plans are thought to be in their early stages, Bloomberg"
            " says that the changes could arrive later this year in iOS 14 and in an update to the HomePod’s firmware."
            " The news comes as Apple is facing increasing antitrust scrutiny over how it manages its platforms. Last "
            "year there were reports that the EU was preparing to launch an antitrust investigation over Spotify’s"
            " complaint that Apple unfairly pushes consumers towards its own music streaming service. Meanwhile in the"
            " US, Bluetooth tracking company Tile recently complained in a congressional antitrust hearing that Apple "
            "unfairly undercuts potential competitors on its platform. "
            "Reports last year claimed Apple could open up its messaging apps. In addition to web browsers and email"
            " clients, Bloomberg also reported last year that Apple was preparing to allow its Siri voice assistant "
            "to send messages via third-party messaging apps by default; meaning you wouldn’t have to specifically"
            " mention them in a voice command. The report also claimed that Apple would later expand this functionality"
            " to phone calls. Apple currently ships around 38 apps with the iPhone and iPad, according to Bloomberg."
            " These can gain a small-yet-significant advantage by being set as the device’s default software installed "
            "on hundreds of millions of iOS and iPadOS devices. Apple has previously said that it includes these apps"
            " to give its users a “great experience right out of the box” and added that there are “many successful "
            "competitors” to its own apps."]

print(get_score(examples))