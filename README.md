[![Codacy Badge](https://app.codacy.com/project/badge/Grade/a1f302d35c0f4f8c9293acabc5086512)](https://app.codacy.com/gh/msmannan00/Orion-Search/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
![CodeQL Analysis](https://github.com/msmannan00/Genesis-Search/actions/workflows/github-code-scanning/codeql/badge.svg)

![homepage](https://github.com/user-attachments/assets/37fcf444-40be-46c9-8bd8-45a22d824141)

# Orion Browser
<table>
<tr>
<td>
<br>
Orion Browser Engine is a web-based search tool built on top of Docker that provides a user-friendly interface to explore and visualize data extracted by the Orion Crawler. The engine supports a vast array of functionalities, offering users the ability to search, filter, and visualize data across multiple categories. It integrates machine learning models for enhanced search relevance and content analysis.
<br>
<br>
</td>
</tr>
<br>
<tr>
<td>
<br>

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

<table>
  <tr>
    <td align="center">
      <img src="https://w7.pngwing.com/pngs/956/695/png-transparent-mongodb-original-wordmark-logo-icon.png" alt="MongoDB" height="50">
      <br>MongoDB
    </td>
    <td align="center">
      <img src="https://upload.wikimedia.org/wikipedia/en/6/6b/Redis_Logo.svg" alt="Redis" height="50">
      <br>Redis
    </td>
    <td align="center">
      <img src="https://docs.celeryproject.org/en/stable/_static/celery_512.png" alt="Celery" height="50">
      <br>Celery
    </td>
    <td align="center">
      <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" height="50">
      <br>Python
    </td>
    <td align="center">
      <img src="https://static1.xdaimages.com/wordpress/wp-content/uploads/2018/09/tor-logo.jpeg" alt="Tor" height="50">
      <br>Tor
    </td>
    <td align="center">
      <img src="https://doc.traefik.io/traefik/assets/img/traefik.logo.png" alt="Traefik" height="50">
      <br>Traefik
    </td>
  </tr>
</table>

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
## Data Extraction Techniques
This is a comprehensive flow diagram illustrating the functioning of the multithreaded crawler. It outlines the entire process, from initializing threads and managing task distribution to efficiently retrieving and processing data from multiple sources concurrently. The diagram highlights key components, such as task queues, thread synchronization mechanisms, and data handling workflows, providing a clear and detailed representation of the crawler's architecture and operational flow

![image(1)](https://github.com/user-attachments/assets/696cf009-a0f3-4995-91fe-58e53b128825)


## Deep Data Linting Roadmap
This document outlines the proposed solution and future roadmap for deep data linting, focusing on integrating insights from multiple sources into a unified platform. The solution emphasizes advanced data validation, cross-source correlation, and seamless integration to ensure comprehensive data quality checks. The roadmap highlights phased development, scalability enhancements, and feature expansions aimed at providing a robust and centralized approach to data insight and linting

![linting(2)](https://github.com/user-attachments/assets/ce1885dc-e701-45f6-89ab-9f412b057373)

### Browser Support

Orion Browser is an Android application designed to provide a secure, private browsing experience by leveraging onion routing technology. This browser empowers users to access hidden web content anonymously, unblock restricted sites, and browse freely while safeguarding their online identity.

![JPJ pdf](https://github.com/user-attachments/assets/399fd130-988d-4e0d-acef-2f60d6220a81)

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

## Project Information

https://www.canva.com/design/DAF8Sa8KkDE/1H8z3RVausdHIMcE98Kvfg/edit
