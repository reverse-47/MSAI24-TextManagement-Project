# MSAI24-TextManagement-Project

## Repository
GitHub: [https://github.com/reverse-47/MSAI24-TextManagement-Project.git](https://github.com/reverse-47/MSAI24-TextManagement-Project.git)

## Course Information
- **Course**: AI6122 Text Data Management & Processing
- **Assignment**: Review Data Analysis and Processing
- **Date**: September 2024
- **Institution**: Nanyang Technological University

## Project Overview
This project involves analyzing the Yelp Open Dataset, focusing on businesses and reviews in Nashville, TN. It includes data processing, indexing, comparison detection, searching, and visualization components.

## Setup Instructions

1. **Dataset Preparation**:
   - Download the Yelp Open Dataset from [https://www.yelp.com/dataset](https://www.yelp.com/dataset).
   - Extract `yelp_academic_dataset_business.json` and `yelp_academic_dataset_review.json` to the `yelp_dataset` folder in the project directory.

2. **Environment Setup**:
   - Ensure Python 3.9+ is installed.
   - Install required packages:
     ```bash
     pip install pandas numpy matplotlib spacy whoosh wordcloud nltk
     ```
   - Download the spaCy English model:
     ```bash
     python -m spacy download en_core_web_sm
     ```
   - Download necessary NLTK data:
     ```python
     import nltk
     nltk.download('punkt')
     ```

3. **Data Preprocessing**:
   - Run the data sampling script to create Nashville-specific subsets:
     ```bash
     python dataset_analysis.ipynb
     ```
   - This will create `Nashville_business_subset.json` and `Nashville_review_subset.json` in the `yelp_dataset` folder.

## Running the Analysis

1. **Detailed Data Analysis**:
   - Open and run `dataset_analysis.ipynb` in a Jupyter Notebook environment for in-depth data exploration and visualizations.

2. **Main Analysis**:
   - Execute the main script:
     ```bash
     python main.py
     ```
   - This will perform indexing, searching, and generate visualizations.

3. **Detecting Comparisons in Reviews**:
   - Execute the comparison detection script with command-line arguments:
     ```bash
     python detect_comparisons.py --review_file yelp_dataset/Nashville_review_subset.json --business_file yelp_dataset/Nashville_business_subset.json --output_file comparison_results.json
     ```
   - **Parameters**:
     - `--review_file`: Path to the JSON file containing reviews.
     - `--business_file`: Path to the JSON file containing business metadata.
     - `--output_file`: Path where the detected comparisons will be saved in JSON format.

   - **Example**:
     ```bash
     python detect_comparisons.py --review_file yelp_dataset/Nashville_review_subset.json --business_file yelp_dataset/Nashville_business_subset.json --output_file comparison_results.json
     ```

## Project Components

- `main.py`: Orchestrates the entire analysis process, including indexing, searching, and visualization.
- `yelp_data_processor.py`: Handles data loading and parsing.
- `yelp_index_processor.py`: Manages indexing of business and review data.
- `yelp_searcher.py`: Implements search functionality (not provided in the given files, but referenced in `main.py`).
- `yelp_review_summarizer.py`: Generates review summaries and visualizations (not provided, but referenced in `main.py`).
- `detect_comparisons.py`: Detects and extracts comparison sentences between businesses in reviews.
- `dataset_analysis.ipynb`: Jupyter notebook for detailed data analysis and visualization.

## Results

- **Detailed Analysis Results**:
  - Available in the `dataset_analysis.ipynb` notebook.

- **Indexing and Search Results**:
  - Located in `output_reference.txt`.

- **Visualizations**:
  - Including the distribution of reviews contributed by users, are generated and saved as `review_distribution.png`.

- **Comparison Detection**:
  - Detected comparisons are saved in `comparison_results.json`.
  - Each entry includes:
    - `review_id`: Unique identifier for the review.
    - `business_id_1`: **Current Review Business**
      - **Description**: The business ID of the business that is the subject of the current review.
    - `business_name_1`: **Current Review Business Name**
      - **Description**: The name of the business being reviewed (`business_id_1`).
    - `business_id_2`: **Compared Business**
      - **Description**: The business ID of another business that the reviewer has previously reviewed and is being compared to the current business.
    - `business_name_2`: **Compared Business Name**
      - **Description**: The name of the business being compared (`business_id_2`).
    - `comparison_sentence`: The sentence from the review where the comparison is made.

  - **Example Entry**:
    ```json
    {
      "review_id": "12345",
      "business_id_1": "abcde",
      "business_name_1": "Pizza Place",
      "business_id_2": "fghij",
      "business_name_2": "Burger Joint",
      "comparison_sentence": "Pizza Place offers better crust compared to Burger Joint."
    }
    ```

## Usage Instructions for `detect_comparisons.py`

1. **Ensure Prerequisites are Met**:
   - All required packages are installed as per the [Environment Setup](#environment-setup) section.
   - The Nashville-specific subsets (`Nashville_business_subset.json` and `Nashville_review_subset.json`) are available in the `yelp_dataset` folder.

2. **Running the Script**:
   - Open your terminal or command prompt.
   - Navigate to the project directory.
   - Execute the script with appropriate arguments:
     ```bash
     python detect_comparisons.py --review_file yelp_dataset/Nashville_review_subset.json --business_file yelp_dataset/Nashville_business_subset.json --output_file comparison_results.json
     ```

3. **Understanding the Output**:
   - The script will generate `comparison_results.json` containing all detected comparisons between businesses.
   - It will also print each comparison to the console in the following format:
     ```
     Review 12345 compares business "Pizza Place" with business "Burger Joint" in the sentence: Pizza Place offers better crust compared to Burger Joint.
     ```

### **Explanation of Output Fields**

- **`business_id_1`**: 
  - **Description**: The business ID of the business that is the subject of the current review.
  - **Role**: Represents the primary business being reviewed in the given review entry.

- **`business_name_1`**:
  - **Description**: The name of the business corresponding to `business_id_1`.
  - **Role**: Provides a human-readable name for the primary business being reviewed.

- **`business_id_2`**:
  - **Description**: The business ID of another business that the reviewer has previously reviewed and is being compared to the current business.
  - **Role**: Identifies the secondary business that is the subject of comparison in the review.

- **`business_name_2`**:
  - **Description**: The name of the business corresponding to `business_id_2`.
  - **Role**: Provides a human-readable name for the secondary business being compared.

- **`comparison_sentence`**:
  - **Description**: The specific sentence from the review where the comparison between `business_name_1` and `business_name_2` is made.
  - **Role**: Highlights the context and content of the comparison, useful for qualitative analysis.

## Additional Notes

- **Adaptability**:
  - The project focuses on Nashville, TN, but can be adapted for other cities by modifying the data sampling process.

- **Search Functionality**:
  - The analysis includes both text-based and geospatial searches.

- **Error Handling**:
  - Ensure that input files are correctly formatted JSON files.
  - The script includes basic error handling, but malformed data may cause interruptions.

- **Extensibility**:
  - Additional scripts and functionalities can be integrated as needed, following the project's modular structure.