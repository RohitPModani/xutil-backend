from fastapi import APIRouter, HTTPException
from ...schemas.text_utilities.lorem_ipsum_schema import LoremIpsumRequest, LoremIpsumResponse, LoremType, OutputFormat
import random

# Common Lorem Ipsum words
LOREM_WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
    "magna", "aliqua", "ut", "enim", "ad", "minim", "veniam", "quis", "nostrud",
    "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea",
    "commodo", "consequat", "duis", "aute", "irure", "dolor", "in", "reprehenderit",
    "in", "voluptate", "velit", "esse", "cillum", "dolore", "eu", "fugiat"
]

# Fixed starting words
STARTING_WORDS = ["Lorem", "ipsum", "dolor", "sit", "amet"]

def generate_lorem_ipsum_logic(data: LoremIpsumRequest) -> LoremIpsumResponse:
    """
    Generate Lorem Ipsum text based on specified type and count, starting with 'Lorem ipsum dolor sit amet'.
    
    Args:
        data: LoremIpsumRequest containing type, count, and format
        
    Returns:
        LoremIpsumResponse with generated text or HTML
        
    Raises:
        HTTPException: If input validation fails or generation fails
    """
    try:
        result = []

        if data.type == LoremType.WORD:
            # Generate count words, starting with STARTING_WORDS
            words = STARTING_WORDS[:min(5, data.count)]  # Use up to count if count < 5
            remaining_words = max(0, data.count - 5)
            if remaining_words > 0:
                words.extend(random.choices(LOREM_WORDS, k=remaining_words))
            result.append(" ".join(words))

        elif data.type == LoremType.SENTENCE:
            # Generate count sentences, first sentence starts with STARTING_WORDS
            for s in range(data.count):
                num_words = random.randint(8, 15)
                sentence = []
                if s == 0:
                    # First sentence starts with STARTING_WORDS
                    sentence.extend(STARTING_WORDS)
                    remaining_words = max(0, num_words - 5)
                    if remaining_words > 0:
                        sentence.extend(random.choices(LOREM_WORDS, k=remaining_words))
                else:
                    sentence.extend(random.choices(LOREM_WORDS, k=num_words))
                if sentence:
                    sentence[0] = sentence[0].capitalize()
                    result.append(" ".join(sentence) + ".")

        elif data.type == LoremType.PARAGRAPH:
            # Generate count paragraphs, first sentence of first paragraph starts with STARTING_WORDS
            for p in range(data.count):
                num_sentences = random.randint(4, 8)
                paragraph = []
                for s in range(num_sentences):
                    num_words = random.randint(8, 15)
                    sentence = []
                    if p == 0 and s == 0:
                        # First sentence of first paragraph starts with STARTING_WORDS
                        sentence.extend(STARTING_WORDS)
                        remaining_words = max(0, num_words - 5)
                        if remaining_words > 0:
                            sentence.extend(random.choices(LOREM_WORDS, k=remaining_words))
                    else:
                        sentence.extend(random.choices(LOREM_WORDS, k=num_words))
                    if sentence:
                        sentence[0] = sentence[0].capitalize()
                        paragraph.append(" ".join(sentence) + ".")
                paragraph_text = " ".join(paragraph)
                if data.format == OutputFormat.HTML:
                    result.append(f"<p>{paragraph_text}</p>")
                else:
                    result.append(paragraph_text)

        # Join results with appropriate separator
        separator = "\n\n" if data.type == LoremType.PARAGRAPH else " "
        if data.type == LoremType.SENTENCE:
            separator = " "
        content = separator.join(result)
        
        if (data.type == LoremType.SENTENCE or data.type == LoremType.WORD) and data.format == OutputFormat.HTML:
            content = "<p>" + content + "</p>"

        return LoremIpsumResponse(content=content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")