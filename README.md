[![Codacy Badge](https://app.codacy.com/project/badge/Grade/a1f302d35c0f4f8c9293acabc5086512)](https://app.codacy.com/gh/msmannan00/Orion-Search/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

![WebApp](https://github.com/msmannan00/Orion-Search/blob/trusted_main/documentation/homepage.png?raw=true)
# Orion Search
<table>
<tr>
<td>
Orion Search Engine is a web-based search tool built on top of Docker that provides a user-friendly interface to explore and visualize data extracted by the Orion Crawler. The engine supports a vast array of functionalities, offering users the ability to search, filter, and visualize data across multiple categories. It integrates machine learning models for enhanced search relevance and content analysis.
</td>
</tr>
<tr>
<td>
📒 Features
<br><br>

**1. Docker-Based Deployment**: Quick setup and deployment using Docker.

**2. Advanced Search Functionality**: Provides comprehensive search capabilities with various filters and options to refine search results.

**3. Data Visualization**: Generates visual representations of the data, making it easier to analyze search results.

**4. Customizable Search Parsers**: Allows for integrating custom parsers to refine data extraction from specific websites.

**5. Integrated Machine Learning Models**: Incorporates NLP and machine learning models to provide search relevance, content categorization, and detection of specific data patterns.
<br><br>
</td>
</tr>
</table>


## Technology Stack

The Orion Search Engine is built using various technologies to provide optimal search capabilities and data handling. Below is the list of libraries and frameworks used:

#### 1. **Search Functionality**

- **elasticsearch==8.15.0**: For indexing and searching data.
- **pymongo==4.8.0**: For handling MongoDB-based data storage.

#### 2. **Web Framework**

- **django==4.2.15**: To provide the web interface and routing.
- **django-bootstrap-v5==1.0.11**: For responsive and modern UI.

#### 3. **Data Processing**

- **pandas==2.1.1**, **numpy==1.26.0**: For efficient data manipulation and analysis.
- **scikit-learn==1.5.1**: For machine learning tasks, such as classification and clustering.
- **gensim==4.3.3**: For natural language processing tasks.

#### 4. **NLP & Similarity Matching**

- **nltk==3.9.0**: For natural language processing tasks and text analysis.
- **html-similarity==0.3.3**: To compare and find similarities between different HTML pages.
- **jaccard-index==0.0.3**: For calculating similarity between sets of data.
- **thefuzz==0.19.0**: Fuzzy string matching for search accuracy.
- **textblob==0.17.1**: For processing textual data, including sentiment analysis.
- **autocorrect==2.6.1**: For automatic text corrections.
- **stopwords==1.0.0**: For handling stopwords in natural language processing.

#### 5. **Networking & Proxies**

- **requests[socks]==2.31.0**, **urllib3==2.1.0**, **PySocks==1.7.1**: For handling proxy-based requests and secure data fetching.
- **stem==1.8.0**: For interacting with Tor.

#### 6. **Data Caching**

- **redis==5.1.1**: For caching search queries and improving performance.

#### 7. **Security & Encryption**

- **cryptography==41.0.3**: For securing sensitive data and communication.

#### 8. **Logging & Monitoring**

- **raven==6.10.0**: For error logging and system monitoring.

#### 9. **Task Management**

- **celery==5.3.4**, **apscheduler==3.10.1**: For managing background tasks, such as indexing and updating search data.

#### 10. **Visualization**

- **Pillow==9.3.0**: For image processing.
- **termcolor==2.3.0**: For colored terminal text output.

#### 11. **Machine Learning & AI**

- **scikit-learn==1.5.1**, **gensim==4.3.3**: For machine learning tasks, such as classification, clustering, and natural language processing.

#### 12. **Additional Libraries**

- **beautifulsoup4==4.12.3**: For parsing and extracting data from HTML and XML documents.
- **lxml==4.9.3**: For processing XML and HTML documents.
- **pyprobables==0.6.0**: For probabilistic data structures like Bloom filters.
- **validators==0.20.0**: For validating URLs and other types of data.
- **simplejson==3.8.0**: For handling JSON data.
- **gunicorn==20.1.0**: For running the application in production.
- **python-dotenv==1.0.0**: For managing environment variables.
- **python-Levenshtein-wheels==0.13.2**: For string matching using the Levenshtein distance.
- **bunch==1.0.0**: For handling grouped data in a Pythonic way.

## Setup and Installation

To get started with Orion Search Engine, follow these steps:

### 1. Clone the Repository

Clone the repository from GitHub and navigate to the project directory.

```
git clone https://github.com/msmannan00/Orion-Search.git
cd Orion-Search
```

## Setup and Installation

To get started with Orion Search, follow these steps:

#### 1. Clone the Repository

Clone the repository from GitHub and navigate to the project directory.

```
https://github.com/msmannan00/Orion-Search.git
cd Orion-Search
```

#### 2. Install Dependencies

Ensure you have Docker and Docker Compose installed on your machine. Once installed, the dependencies will be handled via Docker Compose.

#### 3. Build and Start the Search

Use Docker Compose to build and run the search:

```
./run.sh build
```
to simply start the search run
```
./run.sh
```

This will start the search engine, which can now begin visualizing collected data.

#### 4. Customizing Parsers (Optional for Specific Crawler)

For specific website crawling, you can provide your own parsers. Load them onto the server and configure the crawler to use these custom parsers for enhanced scraping capabilities.
```
add custom parsers inside static/trustly/.well-known/parsers with same onion website name
```


![Screenshot 2![Uploading Deep Data Linting_page-0001.jpg…]()
024-12-05 131938](https://github.com/user-attachments/assets/d5103475-43a8-48e2-a2ce-d4cb2517502a)



## Contribution

We welcome contributions to improve Orion Search. If you'd like to contribute, please fork the repository and submit a pull request.

### Steps to Contribute

1. Fork the repository.  
2. Create a new feature branch (`git checkout -b feature-branch`).  
3. Commit your changes (`git commit -m 'Add some feature'`).  
4. Push to the branch (`git push origin feature-branch`).  
5. Create a new Pull Request.

## License

Orion Search is licensed under the [MIT License](LICENSE).

## Disclaimer

This project is intended for research purposes only. The authors of Orion Search do not support or endorse illegal activities, and users of this project are responsible for ensuring their actions comply with the law.

## GitHub Repository

GitHub Repository URL: [https://github.com/msmannan00/Orion-Search.git](https://github.com/msmannan00/Orion-Search)
