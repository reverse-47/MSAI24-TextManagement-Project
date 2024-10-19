import os
import time
from datetime import datetime
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, NUMERIC, ID, BOOLEAN, KEYWORD, DATETIME
from whoosh.analysis import StemmingAnalyzer, StopFilter, LowercaseFilter
from yelp_data_processor import YelpDataProcessor

class YelpIndexProcessor:
    def __init__(self, index_dir_business, index_dir_review, business_subset_path, review_subset_path):
        self.index_dir_business = index_dir_business
        self.index_dir_review = index_dir_review
        self.custom_stopwords = frozenset(["the", "of", "to", "and", "a", "in", "is", "it", "you", "that",
                                           "he", "was", "for", "on", "are",])
        self.custom_analyzer = StemmingAnalyzer()|StopFilter(stoplist=self.custom_stopwords)|LowercaseFilter()
        
        # Define schema for business data
        self.schema_business = Schema(
            business_id=ID(stored=True, unique=True),
            name=TEXT(stored=True),
            address=TEXT(stored=True),
            city=TEXT(stored=True),
            state=TEXT(stored=True),
            postal_code=ID(stored=True),
            latitude=NUMERIC(stored=True),
            longitude=NUMERIC(stored=True),
            stars=NUMERIC(stored=True),
            review_count=NUMERIC(stored=True),
            is_open=BOOLEAN(stored=True),
            attributes=TEXT(stored=True),
            categories=KEYWORD(stored=True, commas=True),
            hours=TEXT(stored=True)
        )

        # Define schema for review data
        self.schema_review = Schema(
            review_id=ID(stored=True, unique=True),
            user_id=ID(stored=True),
            business_id=ID(stored=True),
            stars=NUMERIC(stored=True),
            useful=NUMERIC(stored=True),
            funny=NUMERIC(stored=True),
            cool=NUMERIC(stored=True),
            text=TEXT(stored=True, analyzer=self.custom_analyzer),
            date=DATETIME(stored=True)
        )

        # Ensure index directories exist
        if not os.path.exists(self.index_dir_business):
            os.mkdir(self.index_dir_business)
        if not os.path.exists(self.index_dir_review):
            os.mkdir(self.index_dir_review)

        # Create indices for business and review data
        self.business_ix = create_in(self.index_dir_business, self.schema_business, indexname="business_index")
        self.review_ix = create_in(self.index_dir_review, self.schema_review, indexname="review_index")

        # Initialize data processor
        self.data_processor = YelpDataProcessor(business_subset_path, review_subset_path)

    def index_business_data(self):
        """Index business data"""
        start_time = time.time()
        writer = self.business_ix.writer()
        business_data = self.data_processor.get_business_data()
        for item in business_data:
            writer.add_document(
                business_id=item['business_id'],
                name=item['name'],
                address=item['address'],
                city=item['city'],
                state=item['state'],
                postal_code=item['postal_code'],
                latitude=item['latitude'],
                longitude=item['longitude'],
                stars=item['stars'],
                review_count=item['review_count'],
                is_open=item['is_open']
            )
        writer.commit()
        index_time = time.time() - start_time
        print("Business data indexed successfully!")
        print(f"Indexing time: {index_time:.2f} seconds")

    def parse_review_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print(f"Invalid date format: {date_str}")
            return None

    def index_review_data_chunks(self, num_batch):
        """Index review data in chunks"""
        review_data = self.data_processor.get_review_data()
        batch_size = len(review_data) // num_batch
        print('batch size:', batch_size)
        review_chunks = [review_data[i:i+batch_size] for i in range(0, 9*batch_size, batch_size)] + [review_data[9*batch_size:]]
        print('num batch', len(review_chunks))

        chunk_time = []
        for index, chunk in enumerate(review_chunks):
            start_time = time.time()
            writer = self.review_ix.writer()

            for item in chunk:
                review_date = self.parse_review_date(item['date'])
                if review_date:
                    writer.add_document(
                        review_id=item['review_id'],
                        user_id=item['user_id'],
                        business_id=item['business_id'],
                        stars=item['stars'],
                        useful=item['useful'],
                        funny=item['funny'],
                        cool=item['cool'],
                        text=item['text'],
                        date=review_date
                    )
            writer.commit()
            index_time = time.time() - start_time
            chunk_time.append(index_time)
            print(f"Review data batch_{index} indexed successfully!")
            print(f"Indexing time: {index_time:.2f} seconds")

        return chunk_time