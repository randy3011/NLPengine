import spacy
from spacy.lang.nl.stop_words import STOP_WORDS
from spacypdfreader import pdf_reader
import PyPDF2
from spacy.cli import evaluate
from string import punctuation
from spacy.scorer import Scorer

#preprocessen
stopwords=list(STOP_WORDS)
punctuation= punctuation+ '\n'

# =============================================================================
# PDF MAKER
# #pdf converter naar txt
# bestand = input('welk pdf wil je uploaden?')
# pdffileobj=open(bestand,'rb')
# pdfreader=pypdf2.pdffilereader(pdffileobj)
# #aantal pagina's
# x=pdfreader.numpages
# #create a variable that will select the selected number of pages
# pageobj=pdfreader.getpage(x+1)
# text=pageobj.extracttext()
# file1=open(r"c:\users\randy\onedrive\bureaublad\ict\jaar 2\blok 3\stage\\1.txt","a")
# file1.writelines(text)
# =============================================================================

#pipeline inlezen met teskt (doc) en NL dataset
text3 = "maakindustrie. >250 medewerkers. >1.500.000. Ja, er wordt data verzameld. De data wordt verzameld op basis van sensoren die doorheen de hele fabriek geplaatst zijn. Downtime, Right first trough, on-time delivery, productie-target. Downtime, Right first trough, productie-target. Ja, wij hebben sensoren die effect hebben op de downtime. Er is een daling van downtime met 80%.  Er zijn bij een aantal machines productinspectie-apparaten aanwezig om dit op peil te houden.  Elke 15 min wordt de downtime gecheckt. Als de downtime niet volgens de richtlijnen is, dan zal de bedrijfsvoering aangepast moeten worden zodat er minimale kostenverlies is.  De bedrijfsvoering wordt aangepast op basis van aandacht op het gebied van de productiemiddelen.  Er is realtime IIOT gegevens beschikbaar om de downtime te meten.  1x per dag. Het gene dat ik zou willen weten, mocht de data automatisch geanalyseerd worden, is hoeveel het effect heeft op het hele productieproces. Daarnaast ook per machine/controlepunt."
text2 = "Energie sector. 250+. Ja. Deze worden opgeslagen op de servers binnen in de fabriek. Deze data wordt gebruikt om te kijken over ergens een proces verbeterd kan worden. Downtime, Right first trough, on-time delivery, productie-target. Welke KPI's zijn afhankelijk van het functioneren van machines? Downtime, Right first trough, productie-target."
text1 = "Het kabinet wil per volgende week vrijdag van de coronapas af, melden het AD, RTL Nieuws en de NOS dinsdag op basis van ingewijden. Wel moet iedereen voor grote binnenevenementen zonder vaste zitplaats met meer dan vijfhonderd bezoekers eerst een coronatest ondergaan. Verbetering: in een eerdere versie van dit bericht stond dat 1G voor álle grote evenementen zou gaan gelden, dus ook buiten. Dat klopt niet: het gaat alleen om binnenevenementen. Volgens de NOS wordt de coronapas alleen nog van stal gehaald als er een situatie ontstaat waarin die echt toegevoegde waarde heeft. Wel kan het zijn dat een coronatoegangsbewijs nog nodig is om naar het buitenland te reizen, omdat andere landen dat als voorwaarde stellen. Het kabinet kiest voor de afschaffing van het coronatoegangsbewijs. Het OMT erkent dat 3G een gering effect heeft, maar zag nog wel heil in de pas, vooral in combinatie met de boosterprik. Op plekken waar een coronapas verplicht is kunnen andere maatregelen, zoals mondkapjes en de anderhalvemeterregel, worden losgelaten. Het kabinet heeft besloten om zowel de coronapas als die andere maatregelen per 25 februari af te schaffen."
nlp = spacy.load('nl_core_news_sm')
nlp1 = spacy.load('nl_core_news_lg')
nlp2 = spacy.load('nl_core_news_md')
doc2 = nlp(text3)
doc1 = nlp1(text3)
doc = nlp2(text3)
#doc1 = pdf_reader('/Users/randy/OneDrive/Bureaublad/ICT/Jaar 2/Blok 3/Stage/.pdf', nlp)

#tokens maken
tokens=[token.text for token in doc]
#print(tokens)


#woord frequencies tellen
woord_frequencies={}
for woord in doc:
    if woord.text.lower() not in stopwords:
        if woord.text.lower() not in punctuation:
            if woord.text not in woord_frequencies.keys():
                woord_frequencies[woord.text] = 1
            else:
                woord_frequencies[woord.text] += 1
#print(woord_frequencies)
max_frequency=max(woord_frequencies.values())
for woord in woord_frequencies.keys():
    woord_frequencies[woord]=woord_frequencies[woord]/max_frequency
#print(woord_frequencies)

zin_tokens= [zin for zin in doc.sents]
#print(sentence_tokens)

zin_scores = {}
for zin in zin_tokens:
    for woord in zin:
        if woord.text.lower() in woord_frequencies.keys():
            if zin not in zin_scores.keys():                            
             zin_scores[zin]=woord_frequencies[woord.text.lower()]
            else:
             zin_scores[zin]+=woord_frequencies[woord.text.lower()]
#print(zin_scores)


#summary maken
from heapq import nlargest
select_lengte=int(len(zin_tokens)*0.3)
summary=nlargest(select_lengte, zin_scores,key=zin_scores.get)
final_summary=[woord.text for woord in summary]
summary=''.join(final_summary)
print(summary)