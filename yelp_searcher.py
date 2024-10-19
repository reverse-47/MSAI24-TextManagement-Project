from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import scoring, index
from math import radians, cos, sin, sqrt, atan2

class YelpSearcher:
    def __init__(self, index_dir, indexname):
        self.index_dir = index_dir
        self.ix = open_dir(self.index_dir, indexname=indexname)

    def search_business(self, query_str):
        """Search for businesses by name"""
        with self.ix.searcher() as searcher:
            query = QueryParser("name", self.ix.schema).parse(query_str)
            results = searcher.search(query)

            print(f"Found {len(results)} results for business name search:")
            for result in results:
                print(f"Business: {result['name']}, City: {result['city']}, State: {result['state']}")

    def search_review(self, query_str, top_n):
        """Search for reviews by content"""
        with self.ix.searcher() as searcher:
            query = QueryParser("text", self.ix.schema).parse(query_str)
            results = searcher.search(query, limit=top_n)

            print(f"Found {len(results)} results for review search:")
            for i, result in enumerate(results):
                print(f"Rank {i + 1}, Score: {result.score}, DocID: {result.docnum}")
                print(f"Review: {result['text']}\n")

class GeoSearch:
    def __init__(self, index_dir):
        self.index_dir = index_dir
        self.R = 6371.0  # Earth's radius in kilometers

    def haversine(self, lat1, lon1, lat2, lon2):
        """Calculate the great circle distance between two points on Earth"""
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return self.R * c  # Returns distance in kilometers

    def geospatial_search(self, lat, lon, radius_km):
        """Perform geospatial search"""
        ix = index.open_dir(self.index_dir, indexname="business_index")
        with ix.searcher(weighting=scoring.BM25F()) as searcher:
            results = searcher.documents()  # Get all businesses
            for result in results:
                distance = self.haversine(lat, lon, result["latitude"], result["longitude"])
                if distance <= radius_km:
                    print(f"Business: {result['name']}, Distance: {distance:.2f} km")

    def combined_search(self, query_str, lat, lon, radius_km):
        """Perform combined text and geospatial search"""
        ix = index.open_dir("indexdir")
        with ix.searcher(weighting=scoring.BM25F()) as searcher:
            parser = MultifieldParser(["review", "name"], schema=ix.schema)
            query = parser.parse(query_str)
            results = searcher.search(query, limit=50)

            filtered_results = []
            for result in results:
                distance = self.haversine(lat, lon, result["latitude"], result["longitude"])
                if distance <= radius_km:
                    filtered_results.append((result, distance))
                    print(f"Business: {result['name']}, Review: {result['review']}, Distance: {distance:.2f} km")

            for i, (result, distance) in enumerate(filtered_results):
                print(f"Rank {i + 1}, DocID: {result.docnum}, Score: {result.score}")
                print(f"Business Name: {result['name']}, Distance: {distance:.2f} km")
                print(f"Review: {result['review']}\n")