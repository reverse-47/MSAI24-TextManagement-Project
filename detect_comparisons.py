import json
import re
import argparse
from nltk.tokenize import sent_tokenize
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict
import nltk

# Download necessary NLTK data
nltk.download('punkt')

# Define keywords that often indicate a comparison
COMPARISON_KEYWORDS = ["better", "worse", "than", "compare", "compared", "best", "worst", "more", "less"]

# Function to detect if a sentence contains a comparison
def contains_comparison(sentence):
    # Check if any comparison keyword is present in the sentence
    for keyword in COMPARISON_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sentence, re.IGNORECASE):
            return True
    return False

# Function to detect if a comparison is between different businesses the reviewer has visited
def is_comparing_with_other_businesses(sentence, business_name_to_id, current_business_id, user_business_dict, user_id):
    # Check if any other business name is explicitly mentioned in the sentence and if the user has visited it
    for business_name, business_id in business_name_to_id.items():
        if (
            business_id != current_business_id and
            business_id in user_business_dict[user_id] and
            re.search(rf"\b{re.escape(business_name)}\b", sentence, re.IGNORECASE)
        ):
            # Additional checks to ensure it's a proper noun and intended as a business name
            if is_business_name_mentioned(sentence, business_name):
                return business_id
    return None

# Function to determine if the business name is mentioned in a way that indicates it is a proper noun
def is_business_name_mentioned(sentence, business_name):
    # Check if the business name appears in quotes, indicating it's a proper noun
    if re.search(rf'["“]{re.escape(business_name)}["”]', sentence):
        return True
    # Check if the business name appears capitalized properly
    if re.search(rf'\b{re.escape(business_name)}\b', sentence):
        words = sentence.split()
        for word in words:
            if word.lower() == business_name.lower() and word[0].isupper():
                return True
    return False

# Function to load business metadata
def load_business_metadata(business_file):
    business_metadata = {}
    business_name_to_id = {}
    with open(business_file, 'r', encoding='utf-8') as file:
        for line in file:
            business = json.loads(line)
            business_metadata[business["business_id"]] = business["name"]
            business_name_to_id[business["name"]] = business["business_id"]
    return business_metadata, business_name_to_id

# Function to create a dictionary of businesses visited by each user
def create_user_business_dict(review_file):
    user_business_dict = defaultdict(set)
    with open(review_file, 'r', encoding='utf-8') as file:
        for line in file:
            review = json.loads(line)
            user_id = review.get("user_id", "")
            business_id = review.get("business_id", "")
            if user_id and business_id:
                user_business_dict[user_id].add(business_id)
    return user_business_dict

# Function to process a chunk of reviews and find comparison sentences
def process_chunk(chunk, business_metadata, business_name_to_id, user_business_dict):
    results = []
    for review in chunk:
        review_text = review.get("text", "")
        business_id = review.get("business_id", "")
        user_id = review.get("user_id", "")
        business_name_1 = business_metadata.get(business_id, "Unknown Business")
        sentences = sent_tokenize(review_text)

        # Find sentences containing comparisons with other businesses
        for sentence in sentences:
            if contains_comparison(sentence):
                compared_business_id = is_comparing_with_other_businesses(
                    sentence, business_name_to_id, business_id, user_business_dict, user_id
                )
                if compared_business_id:
                    compared_business_name = business_metadata.get(compared_business_id, "Unknown Business")
                    results.append({
                        "review_id": review["review_id"],
                        "business_id_1": business_id,
                        "business_name_1": business_name_1,
                        "business_id_2": compared_business_id,
                        "business_name_2": compared_business_name,
                        "comparison_sentence": sentence
                    })
    return results

# Function to read file in chunks
def read_file_in_chunks(file_path, chunk_size=1000):
    with open(file_path, 'r', encoding='utf-8') as file:
        chunk = []
        for line in file:
            chunk.append(json.loads(line))
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

# Main function to find comparisons in reviews using parallel processing
def find_comparisons_in_reviews(review_file, business_file, output_file):
    business_metadata, business_name_to_id = load_business_metadata(business_file)
    user_business_dict = create_user_business_dict(review_file)
    all_results = []
    with ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(process_chunk, chunk, business_metadata, business_name_to_id, user_business_dict): chunk
            for chunk in read_file_in_chunks(review_file)
        }

        for future in as_completed(futures):
            results = future.result()
            all_results.extend(results)

    # Write results to output JSON file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(all_results, outfile, indent=2)

    # Print comparisons between business IDs
    for result in all_results:
        print(f"Review {result['review_id']} compares business \"{result['business_name_1']}\" with business \"{result['business_name_2']}\" in the sentence: {result['comparison_sentence']}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Detect comparisons between businesses in reviews.")
    parser.add_argument(
        "--review_file",
        type=str,
        required=True,
        help="Path to the JSON file containing reviews."
    )
    parser.add_argument(
        "--business_file",
        type=str,
        required=True,
        help="Path to the JSON file containing business metadata."
    )
    parser.add_argument(
        "--output_file",
        type=str,
        required=True,
        help="Path to the output JSON file for detected comparisons."
    )

    # Parse arguments
    args = parser.parse_args()

    # Execute main function with parsed arguments
    find_comparisons_in_reviews(args.review_file, args.business_file, args.output_file)
