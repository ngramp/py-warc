from transformers import pipeline

# Initialize the NER pipeline with a pre-trained model
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", device=0, batch_size=16)

def hug_detect_named_entities(cleaned_content):
    # 0.15secs
    entities = ner_pipeline(cleaned_content)
    org_and_person_entities = [(entity["word"], entity["entity"]) for entity in entities if entity["entity"] in ["I-ORG", "I-PER"]]

    return org_and_person_entities

# Function to detect named entities using Stanford NER
def stanford_detect_named_entities(cleaned_content):
    # 1 sec per record
    doc = nlp(cleaned_content)
    # doc.sentences[0].print_dependencies()


# gpu = spacy.require_gpu()
# print(gpu)
# nlp = spacy.load("en_core_web_sm")

def nltk_detect_named_entities(cleaned_content):
    # 0.5 sec per record
    words = word_tokenize(cleaned_content)
    tagged = pos_tag(words)
    ne = ne_chunk(tagged)
    # Extract organizations and persons
    organizations = []
    persons = []

    for subtree in ne:
        if isinstance(subtree, nltk.Tree):
            entity_type = subtree.label()
            if entity_type == "ORGANIZATION":
                organizations.append(" ".join([word for word, _ in subtree.leaves()]))
            elif entity_type == "PERSON":
                persons.append(" ".join([word for word, _ in subtree.leaves()]))

    # Print recognized organizations and persons
    # print("Organizations:", organizations)
    # print("Persons:", persons)
    return ne


# Function to detect named entities in cleaned content
def spacy_detect_named_entities(cleaned_content):
    # 0.2 sec per record.
    # Process the cleaned content with spaCy NLP pipeline
    doc = nlp(cleaned_content)
    # Extract ORG and PERSON named entities
    org_and_person_entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in {'ORG', 'PERSON'}]

    return org_and_person_entities


# Example usage
if __name__ == "__main__":
    cleaned_content = ("Your cleaned content goes here. Named entities like Apple Inc. and New York City will be "
                       "detected.")
    named_entities = nltk_detect_named_entities(cleaned_content)

    # if named_entities:
    #     print("Named Entities:")
    #     for entity, label in named_entities:
    #         print(f"Entity: {entity}, Label: {label}")
    # else:
    #     print("No named entities detected.")