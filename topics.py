import gensim
import nltk
from gensim import corpora
from nltk.corpus import stopwords
from textblob import TextBlob


nltk.download('stopwords')
def getTopics(filtered_text):
    # Preprocess the text (tokenization, lowercasing, etc.)

    # Tokenize the preprocessed text
    tokens = [word for word in filtered_text.split()]
    stop_words = set(stopwords.words("english"))  # Adjust the language if needed
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Create a Gensim dictionary from the tokens
    dictionary = corpora.Dictionary([filtered_tokens])

    # Create a Gensim corpus
    corpus = [dictionary.doc2bow(filtered_tokens)]

    # Perform topic modeling (e.g., Latent Dirichlet Allocation - LDA)
    lda_model = gensim.models.LdaModel(corpus, num_topics=10, id2word=dictionary)

    # Extract the topics
    topics = lda_model.print_topics(num_words=15)

    # Analyze sentiment for each topic
    topic_sentiments = {}
    for topic_id, topic in topics:
        blob = TextBlob(topic)
        sentiment_score = blob.sentiment.polarity
        topic_sentiments[topic_id] = sentiment_score

    # Categorize topics based on sentiment scores (adjust thresholds as needed)
    positive_topics = [topic_id for topic_id, score in topic_sentiments.items() if score > 0.2]
    negative_topics = [topic_id for topic_id, score in topic_sentiments.items() if score < -0.2]
    neutral_topics = [topic_id for topic_id, score in topic_sentiments.items() if -0.2 <= score <= 0.2]

    # Print or visualize the categorized topics and their sentiment
    print("Positive Topics:", positive_topics)
    print("Negative Topics:", negative_topics)
    print("Neutral Topics:", neutral_topics)

    for topic in topics:
        print("topic:", topic)

    from transformers import pipeline

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Decode the summary tokens into text
    summary = summarizer(filtered_text, max_length=20, min_length=10, do_sample=True)

    print("Generated Summary:")
    print(summary)
    pass

