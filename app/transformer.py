from transformers import pipeline

def main():
    # Initialize the summarization pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Your text to summarize
    text = """In the heart of a bustling city, a spirited Labrador Retriever named Max lives, embodying the essence of loyalty and adventure. Each morning, Max eagerly awaits the soft glow of dawn, his tail wagging like a metronome set to the rhythm of his excitement. His days are filled with the simple joys of life: chasing after the wind's whispers, basking in the warm embrace of the sun, and sharing moments of unconditional love with his human family. Max's presence transforms ordinary days into a tapestry of unforgettable memories, as he teaches those around him the importance of living in the moment. Whether he's bounding through sprawling fields or navigating the urban jungle, Max's adventurous spirit and boundless affection remind us of the profound bond between humans and their canine companions, a bond that transcends words and touches the very soul."""

    # Generate summary
    summary = summarizer(text, max_length=400 , min_length=150 , do_sample=False)

    return summary[0]['summary_text']
