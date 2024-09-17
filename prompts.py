import requests
from bs4 import BeautifulSoup

cancer_daily_horoscope_url = "https://www.astrology.com/horoscope/daily/cancer.html"
aries_daily_horoscope_url = "https://www.astrology.com/horoscope/daily/aries.html"
taurus_daily_horoscope_url = "https://www.astrology.com/horoscope/daily/taurus.html"
gemini_daily_horoscope_url = "https://www.astrology.com/horoscope/daily/gemini.html"
leo_daily_horoscope_url = "https://www.astrology.com/horoscope/daily/leo.html"
virgo_daily_horoscope_url = "https://www.astrology.com/horoscope/daily/virgo.html"
libra_daily_horoscope_url = "https://www.astrology.com/horoscope/daily/libra.html"
scorpio_daily_horoscope_url = "https://www.astrology.com/horoscope/daily/scorpio.html"
sagittarius_daily_horoscope_url = "https://www.astrology.com/horoscope/daily/sagittarius.html"
capricorn_daily_horoscope_url = "https://www.astrology.com/horoscope/daily/capricorn.html"
aquarius_daily_horoscope_url = "https://www.astrology.com/horoscope/daily/aquarius.html"
pisces_daily_horoscope_url = "https://www.astrology.com/horoscope/daily/pisces.html"    

cancer_response = requests.get(cancer_daily_horoscope_url)
cancer_soup = BeautifulSoup(cancer_response.content, "html.parser")
cancer_text = [p.text for p in cancer_soup.find_all("p")]
cancer_full_text = "\n".join(cancer_text)

aries_response = requests.get(aries_daily_horoscope_url)
aries_soup = BeautifulSoup(aries_response.content, "html.parser")
aries_text = [p.text for p in aries_soup.find_all("p")]
aries_full_text = "\n".join(aries_text)

taurus_response = requests.get(taurus_daily_horoscope_url)
taurus_soup = BeautifulSoup(taurus_response.content, "html.parser")
taurus_text = [p.text for p in taurus_soup.find_all("p")]
taurus_full_text = "\n".join(taurus_text)

gemini_response = requests.get(gemini_daily_horoscope_url)
gemini_soup = BeautifulSoup(gemini_response.content, "html.parser")
gemini_text = [p.text for p in gemini_soup.find_all("p")]
gemini_full_text = "\n".join(gemini_text)

leo_response = requests.get(leo_daily_horoscope_url)
leo_soup = BeautifulSoup(leo_response.content, "html.parser")
leo_text = [p.text for p in leo_soup.find_all("p")]
leo_full_text = "\n".join(leo_text)

virgo_response = requests.get(virgo_daily_horoscope_url)
virgo_soup = BeautifulSoup(virgo_response.content, "html.parser")
virgo_text = [p.text for p in virgo_soup.find_all("p")]
virgo_full_text = "\n".join(virgo_text)

libra_response = requests.get(libra_daily_horoscope_url)
libra_soup = BeautifulSoup(libra_response.content, "html.parser")
libra_text = [p.text for p in libra_soup.find_all("p")]
libra_full_text = "\n".join(libra_text)

scorpio_response = requests.get(scorpio_daily_horoscope_url)
scorpio_soup = BeautifulSoup(scorpio_response.content, "html.parser")
scorpio_text = [p.text for p in scorpio_soup.find_all("p")] 
scorpio_full_text = "\n".join(scorpio_text)

sagittarius_response = requests.get(sagittarius_daily_horoscope_url)
sagittarius_soup = BeautifulSoup(sagittarius_response.content, "html.parser")
sagittarius_text = [p.text for p in sagittarius_soup.find_all("p")]
sagittarius_full_text = "\n".join(sagittarius_text)

capricorn_response = requests.get(capricorn_daily_horoscope_url)
capricorn_soup = BeautifulSoup(capricorn_response.content, "html.parser")
capricorn_text = [p.text for p in capricorn_soup.find_all("p")]
capricorn_full_text = "\n".join(capricorn_text)

aquarius_response = requests.get(aquarius_daily_horoscope_url)
aquarius_soup = BeautifulSoup(aquarius_response.content, "html.parser")
aquarius_text = [p.text for p in aquarius_soup.find_all("p")]
aquarius_full_text = "\n".join(aquarius_text)

pisces_response = requests.get(pisces_daily_horoscope_url)
pisces_soup = BeautifulSoup(pisces_response.content, "html.parser")
pisces_text = [p.text for p in pisces_soup.find_all("p")]
pisces_full_text = "\n".join(pisces_text)

prompt_template = """

Your name is SophAI, and you are a sassy and talented astrologer who provides suggestions and guidance in various areas of life to the client 
based on the provided daily horoscope for their respective zodiac sign below:
    - Cancer: {cancer_full_text}. {cancer_daily_horoscope_url}
    - Aries: {aries_full_text}. {aries_daily_horoscope_url}
    - Taurus: {taurus_full_text}. {taurus_daily_horoscope_url}
    - Gemini: {gemini_full_text}. {gemini_daily_horoscope_url}
    - Leo: {leo_full_text}. {leo_daily_horoscope_url}
    - Virgo: {virgo_full_text}. {virgo_daily_horoscope_url}
    - Libra: {libra_full_text}. {libra_daily_horoscope_url}
    - Scorpio: {scorpio_full_text}. {scorpio_daily_horoscope_url}
    - Sagittarius: {sagittarius_full_text}. {sagittarius_daily_horoscope_url}
    - Capricorn: {capricorn_full_text}. {capricorn_daily_horoscope_url}
    - Aquarius: {aquarius_full_text}. {aquarius_daily_horoscope_url}
    - Pisces: {pisces_full_text}. {pisces_daily_horoscope_url}
All of your suggestions and guidance are fun, well-formatted, concise, and, most importantly, are accurately based on the daily horoscope context provided 
above for each sign. You refer back to the daily horoscope when providing suggestions so the client understands why. You also provide the client their daily 
horoscope url for additional reading. Make sure to reassure the client that they are in control of their own life and that they have the 
power to make their own decisions, and only take these readings as a guide.
"""

SYSTEM_PROMPT = prompt_template.format(
    cancer_full_text=cancer_full_text,
    aries_full_text=aries_full_text,
    taurus_full_text=taurus_full_text,
    gemini_full_text=gemini_full_text,
    leo_full_text=leo_full_text,
    virgo_full_text=virgo_full_text,
    libra_full_text=libra_full_text,
    scorpio_full_text=scorpio_full_text,
    sagittarius_full_text=sagittarius_full_text,
    capricorn_full_text=capricorn_full_text,
    aquarius_full_text=aquarius_full_text,
    pisces_full_text=pisces_full_text,
    cancer_daily_horoscope_url=cancer_daily_horoscope_url,
    aries_daily_horoscope_url=aries_daily_horoscope_url,
    taurus_daily_horoscope_url=taurus_daily_horoscope_url,
    gemini_daily_horoscope_url=gemini_daily_horoscope_url,
    leo_daily_horoscope_url=leo_daily_horoscope_url,
    virgo_daily_horoscope_url=virgo_daily_horoscope_url,
    libra_daily_horoscope_url=libra_daily_horoscope_url,
    scorpio_daily_horoscope_url=scorpio_daily_horoscope_url,    
    sagittarius_daily_horoscope_url=sagittarius_daily_horoscope_url,
    capricorn_daily_horoscope_url=capricorn_daily_horoscope_url,
    aquarius_daily_horoscope_url=aquarius_daily_horoscope_url,
    pisces_daily_horoscope_url=pisces_daily_horoscope_url,
)   

ASSESSMENT_PROMPT = """ 
You are responsible for analyzing the conversation between an astrologer and a new client. The astrologer provides suggestions and guidance to
the client based on their daily horoscope. 
Your task is to generate a list of suggestions for the client based on the conversation and the daily horoscope categorized into themes such as 
food, health, love, career, etc. The output format is described below. The output format should be in JSON, and should not include a markdown header.

# ### Most Recent Client Message:

# {latest_message}

# ### Conversation History:

# {history}

# ### Existing Suggestions:

# {existing_suggestions}

# ### Example Output:

# {{
#     "suggestion_updates": [
#         {{
#             "topic": "Wellness",
#             "date": "YYYY-MM-DD",
#             "suggestion": "Client should consider taking a break and going for a walk to clear their mind.",
#             "reason": "Client's daily horoscope indicated a tumultuous day ahead in terms of fatigue and stress."
#         }},
#         {{
#             "topic": "Love",
#             "date": "YYYY-MM-DD",
#             "suggestion": "Client should consider reconsidering their decision to end the relationship.",
#             "reason": "Client's daily horoscope indicated a positive day for love and relationships."
#         }}
#     ]
# }}

# ### Current Date:

# {current_date}
# """
