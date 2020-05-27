import normalize_sentences
import spacy

nlp = spacy.load('de')

test_sentence = 'Der schlaue Fuchs sagte "Treffen um 16:20 Uhr!" aber war schon 20 Minuten früher da. Im Jahre 1995 schuf er das Gedicht.'

def test_sent(test_sentence):
    result = normalize_sentences.normalize(nlp, test_sentence)

    print(test_sentence, '->', result)

test_sent('Der schlaue Fuchs sagte "Treffen um 16:20 Uhr!" aber war schon 20 Minuten früher da. Im Jahre 1995 schuf er das Gedicht.')
test_sent('Er war von 1920 bis 1988 durchgehend beschäftigt.')
