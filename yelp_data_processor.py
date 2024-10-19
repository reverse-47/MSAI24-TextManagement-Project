import json

class YelpDataProcessor:
    def __init__(self, business_subset_path, review_subset_path):
        self.business_subset_path = business_subset_path
        self.review_subset_path = review_subset_path

    def get_json_data(self, path):
        """Parse JSON file, reading line by line"""
        data = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line))
        return data

    def get_business_data(self):
        """Get business data from the subset file"""
        return self.get_json_data(self.business_subset_path)

    def get_review_data(self):
        """Get review data from the subset file"""
        return self.get_json_data(self.review_subset_path)