# MSAI24-TextManagement-Project

## Course Information
- Course: AI6122 Text Data Management & Processing
- Assignment: Review Data Analysis and Processing
- Date: September 2024
- Institution: Nanyang Technological University

## Project Overview
This project involves analyzing the Yelp Open Dataset, focusing on businesses and reviews in Nashville, TN. It includes data processing, indexing, searching, and visualization components.

## Setup Instructions

1. **Dataset Preparation**:
   - Download the Yelp Open Dataset from [https://www.yelp.com/dataset](https://www.yelp.com/dataset)
   - Extract `yelp_academic_dataset_business.json` and `yelp_academic_dataset_review.json` to the `yelp_dataset` folder in the project directory

2. **Environment Setup**:
   - Ensure Python 3.9+ is installed
   - Install required packages:
     ```
     pip install pandas numpy matplotlib spacy whoosh wordcloud
     ```
   - Download the spaCy English model:
     ```
     python -m spacy download en_core_web_sm
     ```

3. **Data Preprocessing**:
   - Run the data sampling script to create Nashville-specific subsets:
     ```
     python dataset_analysis.ipynb
     ```
   - This will create `Nashville_business_subset.json` and `Nashville_review_subset.json` in the `yelp_dataset` folder

## Running the Analysis

1. **Main Analysis**:
   - Execute the main script:
     ```
     python main.py
     ```
   - This will perform indexing, searching, and generate visualizations

2. **Detailed Data Analysis**:
   - Open and run `dataset_analysis.ipynb` in a Jupyter Notebook environment for in-depth data exploration and visualizations

## Project Components

- `main.py`: Orchestrates the entire analysis process
- `yelp_data_processor.py`: Handles data loading and parsing
- `yelp_index_processor.py`: Manages indexing of business and review data
- `yelp_searcher.py`: Implements search functionality (not provided in the given files, but referenced in `main.py`)
- `yelp_review_summarizer.py`: Generates review summaries and visualizations (not provided, but referenced in `main.py`)
- `dataset_analysis.ipynb`: Jupyter notebook for detailed data analysis and visualization

## Results

- Indexing and search results can be found in `output_reference.txt`
- Visualizations, including the distribution of reviews contributed by users, are generated and saved as image files
- Detailed analysis results are available in the `dataset_analysis.ipynb` notebook

## Notes

- The project focuses on Nashville, TN, but can be adapted for other cities by modifying the data sampling process
- The analysis includes both text-based and geospatial searches
- Performance metrics for indexing and searching are provided in the output

For any questions or issues, please refer to the assignment instructions or contact the course instructor.
