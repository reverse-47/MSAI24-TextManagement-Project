from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from collections import Counter, defaultdict
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import nltk
import matplotlib.pyplot as plt

nltk.download('punkt')
nltk.download('stopwords')

class YelpReviewSummarizer:
    def __init__(self, index_dir_review, index_dir_business):
        self.index_dir_review = index_dir_review
        self.index_dir_business = index_dir_business
        self.stop_words = set(stopwords.words('english'))

    def plot_review_distribution(self):
        ix_review = open_dir(self.index_dir_review, indexname="review_index")
        
        with ix_review.searcher() as searcher:
            # Get all user IDs and their review counts
            user_review_counts = defaultdict(int)
            for doc in searcher.documents():
                user_review_counts[doc['user_id']] += 1
            
            # Calculate the number of users for each review count
            review_count_distribution = defaultdict(int)
            for count in user_review_counts.values():
                review_count_distribution[count] += 1
            
            # Prepare plotting data
            x = list(review_count_distribution.keys())
            y = list(review_count_distribution.values())

            # Plot the chart
            plt.figure(figsize=(12, 6))
            plt.scatter(x, y, alpha=0.5)
            plt.xlabel('Number of reviews contributed by a user')
            plt.ylabel('Number of users')
            plt.title('Distribution of reviews contributed by users')
            plt.xscale('symlog', linthresh=1)
            plt.yscale('symlog', linthresh=1)
            plt.grid(True)
            
            # Add annotations for specific points
            for point in [10, 20, 30, 50, 100]:
                if point in review_count_distribution:
                    plt.annotate(f'({point}, {review_count_distribution[point]})', 
                                 (point, review_count_distribution[point]),
                                 xytext=(5, 5), textcoords='offset points')
            
            plt.savefig('review_distribution.png')
            print("Review distribution plot saved as 'review_distribution.png'")

    def get_user_review_summary(self, user_id):
        ix_review = open_dir(self.index_dir_review, indexname="review_index")
        ix_business = open_dir(self.index_dir_business, indexname="business_index")

        with ix_review.searcher() as searcher_review, ix_business.searcher() as searcher_business:
            # Get user review count
            user_query = QueryParser("user_id", ix_review.schema).parse(user_id)
            results = searcher_review.search(user_query, limit=None)
            review_count = len(results)

            # Get user activity area
            business_ids = set(result['business_id'] for result in results)
            min_lat, max_lat, min_lon, max_lon = float('inf'), float('-inf'), float('inf'), float('-inf')
            for business_id in business_ids:
                business_query = QueryParser("business_id", ix_business.schema).parse(business_id)
                business_results = searcher_business.search(business_query)
                if business_results:
                    business = business_results[0]
                    min_lat = min(min_lat, business['latitude'])
                    max_lat = max(max_lat, business['latitude'])
                    min_lon = min(min_lon, business['longitude'])
                    max_lon = max(max_lon, business['longitude'])

            # Get frequent words and phrases
            all_words = []
            all_text = ""
            for result in results:
                words = [word.lower() for word in result['text'].split() if word.lower() not in self.stop_words]
                all_words.extend(words)
                all_text += result['text'] + " "

            top_words = Counter(all_words).most_common(10)
            
            # Get representative sentences (simple method: choose sentences containing the most frequent words)
            sentences = sent_tokenize(all_text)
            sentence_scores = [(sentence, sum(word in sentence.lower() for word, _ in top_words)) for sentence in sentences]
            representative_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:3]

        return {
            "review_count": review_count,
            "bounding_box": (min_lat, max_lat, min_lon, max_lon),
            "top_words": top_words,
            "representative_sentences": [sentence for sentence, _ in representative_sentences]
        }

    def print_user_review_summary(self, user_id):
        summary = self.get_user_review_summary(user_id)
        print(f"User Review Summary for user_id: {user_id}")
        print(f"Number of reviews: {summary['review_count']}")
        print(f"Activity area (bounding box): {summary['bounding_box']}")
        print("Top 10 most frequent words:")
        for word, count in summary['top_words']:
            print(f"  {word}: {count}")
        print("Three most representative sentences:")
        for i, sentence in enumerate(summary['representative_sentences'], 1):
            print(f"  {i}. {sentence}")