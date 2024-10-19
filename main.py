from yelp_index_processor import YelpIndexProcessor
from yelp_searcher import YelpSearcher, GeoSearch
from yelp_review_summarizer import YelpReviewSummarizer

# Set paths
path_business_subset = 'yelp_dataset/Nashville_business_subset.json'
path_review_subset = 'yelp_dataset/Nashville_review_subset.json'
index_dir_business = "indexdir_business"
index_dir_review = "indexdir_review"

# Set search parameters
search_business_keyword = 'Pizza'
search_geo_point = (36.115118, -86.766925)  # latitude, longitude
search_radius_km = 0.5
search_review_keyword = 'coffee'
top_n = 5
num_batch = 10  # Required: 10% of reviews

# Add user ID parameter
user_id_for_summary = "DW6dmaJHHCz2RPHh6PuMLg"

if __name__ == "__main__":
    # Create index
    processor_index = YelpIndexProcessor(index_dir_business, index_dir_review, path_business_subset, path_review_subset)

    print('Indexing business data')
    processor_index.index_business_data()
    print('--------------------')
    print(f'Searching keyword: {search_business_keyword}')
    searcher_business = YelpSearcher(index_dir_business, indexname='business_index')
    searcher_business.search_business(search_business_keyword)
    print('--------------------')
    print(f'Geospatial search: Businesses within {search_radius_km}km of {search_geo_point}')
    geo_searcher = GeoSearch(index_dir_business)
    geo_searcher.geospatial_search(search_geo_point[0], search_geo_point[1], search_radius_km)

    print('--------------------')
    print('Indexing review data')
    processor_index.index_review_data_chunks(num_batch=num_batch)
    print('--------------------')
    print(f'Searching keyword: {search_review_keyword}')
    searcher_review = YelpSearcher(index_dir_review, indexname='review_index')
    searcher_review.search_review(search_review_keyword, top_n=top_n)

    # Generate review distribution plot
    print('--------------------')
    print('Generating review distribution plot')
    review_summarizer = YelpReviewSummarizer(index_dir_review, index_dir_business)
    review_summarizer.plot_review_distribution()

    # Generate user review summary
    print('--------------------')
    print('Generating user review summary')
    review_summarizer.print_user_review_summary(user_id_for_summary)