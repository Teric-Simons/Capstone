from transformers import pipeline

def main(text):
    # Initialize the summarization pipeline
    summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    tokenizer="sshleifer/distilbart-cnn-12-6"
)

    summary = summarizer(
        text,
        max_length=1024,  # Adjust according to your desired length
        min_length=350,
        do_sample=True,
        num_beams=4,
        length_penalty=2.0
)



    # Generate summary
    

    return summary[0]['summary_text']
