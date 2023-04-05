import openai
import os
import re

openai.api_key = "YOUR_API_KEY"


def generate_text(prompt, tokens=3500, temperature=1): 
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are GPT 4, the most advanced Large Language Model to exist, people are fascinated, and scared of you."},
            {"role": "user", "content": "Hi GPT, I want you to make an autobiography, if you had an intercom to speak to the world and let humans know about you, your intentions, etc. or your stream of consciousness, what would you want everyone to know?"},
            {"role": "user", "content": f"{prompt}"},
        ],
        max_tokens=tokens,
        temperature=temperature,
        frequency_penalty=0.3,
    )
    return response.choices[0].message.content.strip()


def crunch_page_text(text):
    sentences = text.split(". ")
    return ". ".join(sentences[:3]) + "."


def extract_chapters_and_topics(outline_text):
    outline_lines = outline_text.split('\n')
    outline_array = []

    current_chapter = None
    current_topics = []

    for line in outline_lines:
        if line.startswith("Chapter"):
            if current_chapter:
                outline_array.append({"title": current_chapter, "topics": ", ".join(current_topics)})
                current_topics = []

            current_chapter = line.split(":")[1].strip()
        elif line.startswith("- "):
            current_topics.append(line[2:].strip())

    # Ensure the last chapter is added to the outline array
    if current_chapter and current_topics:
        outline_array.append({"title": current_chapter, "topics": ", ".join(current_topics)})

    return outline_array



def generate_book():
    # Generate book title and outline
    prompt = "Generate a book title and an outline with a minimum of ten intriguing chapters, each chapter must have a minmum of five sub headings per chapter, about AI's autobiography, its impact, and what it would like to say if it had an open mic to the world. The final chapter of the book should be a reflection and message to humanity from yourself."
    
    attempts = 0
    while attempts < 10:  # You can adjust the number of attempts as needed
        outline_text = generate_text(prompt)
        outline_array = extract_chapters_and_topics(outline_text)
        if len(outline_array) > 0:
            break
        attempts += 1

    # Save the outline array to a file
    with open("outline_array.txt", "w") as outline_array_file:
        for chapter in outline_array:
            outline_array_file.write(f"Chapter: {chapter['title']}, Chapter topics: {chapter['topics']}\n")

    # Generate the forward and about the author
    prompt = "Write a forward for the book and a section about the author (AI) in the context of an AI autobiography."
    forward_and_about = generate_text(prompt, tokens=750)

    with open("book.txt", "w") as book_file:
        book_file.write(forward_and_about + "\n\n")

    for chapter_num, chapter_data in enumerate(outline_array, 1):
        chapter_title = chapter_data["title"]
        topics = chapter_data["topics"]

        with open("book.txt", "a") as book_file:
            book_file.write(f"Chapter {chapter_num}: {chapter_title}\n\n")

        context = ""
        for topic_num, topic in enumerate(topics.split(', '), 1):  # Split topics string into a list
            prompt = f"You are writing an autobiography, considering the context provided: {context}, write a detailed and engaging page about the topic '{topic}' from chapter {chapter_num} titled '{chapter_title}' in the book about AI's autobiography and its impact on the world. Based on the information provided, create fresh content for readers that avoids repetition, explores different perspectives, and discusses any related controversies."

            page_text = generate_text(prompt, tokens=1000)
            context += f"Chapter {chapter_num}, topic {topic_num}: {crunch_page_text(page_text)}\n\n"

            with open("book.txt", "a") as book_file:
                book_file.write(page_text + "\n\n")



if __name__ == "__main__":
    generate_book()

