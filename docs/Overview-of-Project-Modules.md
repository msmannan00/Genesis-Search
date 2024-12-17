# Data Intelligence Platform Documentation

## Introduction

This documentation provides an extensive overview of our Data Intelligence Platform, a comprehensive suite of tools and services designed to streamline the process of discovering, collecting, indexing, and analyzing data from various open, deep, and dark web sources. The platform is divided into two major sections:

- **Active Intelligence:** Focused on proactive data collection, indexing, and visualization using automated crawlers, search infrastructure, and integrated browser technology.
- **Passive Intelligence:** Geared towards whistle-blowing and anonymous data submission capabilities, leveraging established open-source frameworks for secure and anonymous reporting.

Each component within these sections plays a unique role, contributing to the platform’s overarching goal: enabling researchers, OSINT (Open Source Intelligence) analysts, investigative journalists, and developers to efficiently gather actionable intelligence from difficult-to-access sources.

---

## Active Intelligence

### Overview

Active Intelligence encompasses a set of tools that actively reach out to hidden, multilayered web services, crawl their content, and present that data for indexing, analysis, and visualization. These tools are designed to operate in tandem, forming an integrated pipeline where data flows from initial discovery, through processing and indexing, to final visualization.

**Key Highlights:**
- Automated, intelligent crawling of hidden services (Onion, I2P, etc.)
- Machine learning-driven data extraction and classification
- High-performance indexing and search capabilities
- Seamless integration for custom data collection scripts
- Browser-based exploration with built-in anonymity features

The Active Intelligence suite is composed of four main submodules:

1. **Orion Crawler**
2. **Orion Search**
3. **Orion Browser**
4. **Orion Collector**

---

### Orion Crawler

**Purpose:**  
The Orion Crawler is the starting point of the active intelligence pipeline. Its primary role is to automatically navigate through various hidden and anonymous networks (like Onion and I2P), scraping raw data from websites and forums that are not easily accessible by conventional search engines.

**Key Features:**
- **Multithreading:** Implements Python’s concurrency capabilities and Celery distributed task queue to handle multiple crawl tasks in parallel, improving efficiency and throughput.
- **Machine Learning Integration:** Utilizes ML-based classification models to filter relevant content, prioritize high-value targets, and adaptively refine crawl strategies over time.
- **Scalable Architecture:** Easily add more workers to the Celery queue to handle increased crawling demands.
- **Modular Design:** Pluggable components allow for integration with different data sources and protocols beyond Onion and I2P (e.g., ZeroNet, Freenet).

**Technology Stack:**
- **Language & Framework:** Python + Celery
- **Data Storage:** Initial raw data dumps to local or distributed storage (e.g., AWS S3, MinIO, or local filesystem)
- **ML Models:** Python-based (TensorFlow/PyTorch/Scikit-learn) classification and entity extraction models

**Workflow:**
1. **Target Seed Input:** Provide a list of seed URLs or services.
2. **Distributed Task Queue:** Orion Crawler workers fetch tasks from the Celery queue.
3. **Content Extraction:** The crawler retrieves HTML, images, documents, or other file types.
4. **ML-driven Filtering:** Extracted content runs through ML models for classification, relevance scoring, and entity extraction.
5. **Storage & Indexing Prep:** Cleaned, structured data is stored for indexing by Orion Search.

---

### Orion Search

**Purpose:**  
Orion Search provides a powerful, fast, and scalable search interface on top of the collected and processed data. By leveraging the indexing capabilities of Elasticsearch, it allows users to quickly query, filter, and visualize insights from massive datasets.

**Key Features:**
- **High-Performance Indexing:** Swift ingestion of data from Orion Crawler’s output into Elasticsearch indices.
- **Advanced Querying:** Support for full-text search, keyword queries, fuzzy matches, and complex Boolean queries.
- **Faceted Navigation:** Drill down through content by tags, categories, timeframes, or any metadata field.
- **Data Visualization:** Integration with Kibana or custom dashboards for charts, graphs, and timeline views.

**Technology Stack:**
- **Search Engine:** Elasticsearch
- **Indexing Connectors:** Python-based indexing scripts that batch-process crawler output.
- **Visualization:** Kibana or custom front-end interfaces.

**Workflow:**
1. **Ingestion:** Processed data from Orion Crawler is fed into Elasticsearch.
2. **Index Refresh:** Automated index refresh intervals ensure newly ingested data is queryable with minimal delay.
3. **Query & Analysis:** Users or downstream systems query Elasticsearch for specific intelligence needs.
4. **Visualization:** Results can be displayed in interactive dashboards or integrated into analytical workflows.

---

### Orion Browser

**Purpose:**  
The Orion Browser is a specialized Android-based browser designed to function as a data harvester. While Orion Crawler proactively fetches data programmatically, Orion Browser complements this by allowing human-driven navigation. As an analyst browses through target websites, Orion Browser automatically indexes and scrapes encountered data, creating a feedback loop for more in-depth exploration.

**Key Features:**
- **Android-Native Integration:** Built with Kotlin and Java, utilizing Orbot libraries for Tor network integration to maintain anonymity.
- **Automated Harvesting:** As the analyst navigates the site, Orion Browser extracts content, metadata, and structural information behind the scenes.
- **Seamless Indexing:** Harvested data is sent back to the indexing pipeline for subsequent searching and analysis.
- **Customizable Plugins:** Extend functionality through custom plugins for additional data extraction techniques or browser automation.

**Technology Stack:**
- **Platform:** Android
- **Languages:** Kotlin, Java
- **Privacy & Anonymity:** Orbot integration to route traffic through Tor
- **Data Extraction:** Local scraping tools integrated into the browser’s rendering engine

**Workflow:**
1. **Analyst Browsing:** User navigates dark web marketplaces, forums, or hidden services using the Orion Browser.
2. **Real-Time Extraction:** Each visited page is scraped, text and metadata are extracted.
3. **Metadata Packaging:** Structured content is packaged and securely sent to the indexing pipeline.
4. **Index Integration:** The newly harvested data appears in Orion Search after re-indexing, allowing quick retrieval and analysis.

---

### Orion Collector

**Purpose:**  
The Orion Collector streamlines the integration of custom collection scripts and scraping configurations. Instead of requiring extensive setup for each new target site, developers and OSINT engineers can simply modify or submit new scripts tailored to specific sources. The Orion Collector automates the rest, handling ingestion, extraction, and indexing without manual reconfiguration.

**Key Features:**
- **Script-Based Customization:** Developers create or modify scraper scripts in a standardized format.
- **Pull Request Integration:** Submit a pull request with new or updated scripts; once merged, the platform automatically incorporates the changes.
- **Auto-Configuration:** No additional manual configuration required. The Collector dynamically loads and applies new scripts, ensuring smooth scaling to multiple, specialized data sources.
- **Developer-Friendly:** Clear documentation, code templates, and examples help reduce the learning curve for contributing engineers.

**Technology Stack:**
- **Core Language:** Python (for ingestion and script execution)
- **Version Control:** Git-based workflow to track and merge changes to scraper scripts
- **Continuous Integration (CI):** Automated testing of new scripts before deploying them into production
- **Script Templates:** YAML/JSON configurations plus Python-based scraping logic

**Workflow:**
1. **Script Creation:** Developer creates a new scraper script targeting a specific site or data type.
2. **Pull Request & Review:** Developer submits a PR. Code reviewers ensure script quality and compatibility.
3. **Merge & Deploy:** Once approved, changes are merged, and the Collector automatically loads the new script.
4. **Data Pipeline Update:** The newly configured script runs within the existing pipeline, adding its data to Orion Search.

---

## Passive Intelligence

### Overview

While Active Intelligence focuses on proactive data gathering, Passive Intelligence centers around securely receiving and managing whistleblowing submissions. In situations where anonymous individuals need a safe channel to leak documents or reveal information, the Passive Intelligence section provides a robust platform built on top of proven whistleblowing frameworks.

**Key Highlights:**
- Secure, anonymous submission channels for sensitive documents or evidence
- Established, open-source foundations for whistleblowing functionality
- Integrated workflows that allow for external data to complement the Active Intelligence datasets

### Whistleaks

**Purpose:**  
Whistleaks is a whistleblowing platform implemented atop the Globaleaks framework. It provides a secure environment for sources to submit sensitive documents and information without revealing their identities. Whistleblowers can trust the platform’s encryption, anonymity, and metadata stripping features, ensuring maximum confidentiality and protection.

**Key Features:**
- **Globaleaks Integration:** Leverages Globaleaks’ robust anonymity tools, onion routing, and secure communication channels.
- **Strong Encryption:** Ensures that all submitted data is encrypted at rest and in transit.
- **Metadata Anonymization:** Removes identifying information from uploaded files before storing them.
- **Source Protection:** Utilizes Tor hidden services and secure browsers to prevent source fingerprinting.

**Technology Stack:**
- **Base Framework:** Globaleaks
- **Security & Anonymity:** Tor integration, secure TLS configurations
- **User Interface:** Web-based submission portal accessible via Tor browser or other anonymity tools

**Workflow:**
1. **Whistleblower Submission:** The source accesses the Whistleaks portal via a Tor hidden service.
2. **Document Upload & Metadata Stripping:** The submitted files are automatically cleaned of identifying metadata.
3. **Encrypted Storage:** All documents are stored securely, awaiting review by authorized analysts.
4. **Review & Analysis:** Approved analysts review submissions, cross-referencing them with data from the Active Intelligence suite to build a comprehensive intelligence picture.

---

## Integration & Data Flow

**End-to-End Pipeline Example:**
1. **Active Collection:** Orion Crawler systematically collects large volumes of hidden web content.  
2. **Browsing & Refinement:** Analysts explore leads using Orion Browser, adding contextually relevant data as they navigate.  
3. **Automated Indexing:** Orion Search indexes newly acquired data, making it searchable and analyzable.  
4. **Script Customization:** Developers add specialized scrapers to Orion Collector for niche sites, further enriching the dataset.  
5. **Passive Contributions:** Whistleblowers submit sensitive documents to Whistleaks, providing insider information that complements the crawled and indexed datasets.  
6. **Holistic Analysis:** By combining actively collected data with passively provided whistleblower documents, analysts gain a complete, multidimensional understanding of their targets, leading to actionable intelligence insights.

---

## Deployment & Maintenance

**Recommended Practices:**
- **Containerization:** Deploy Orion Crawler, Collector, and Search indexing components using Docker or Kubernetes for scalable, repeatable environments.
- **Continuous Integration & Deployment (CI/CD):** Use CI/CD pipelines to test new scripts, crawler configurations, and upgrades to ensure stability.
- **Security Hardening:** Regularly update dependencies, apply Tor configuration best practices, and audit logs to maintain secure operations.
- **Backups & Redundancy:** Regularly back up indexes, ML model states, and whistleblowing submissions. Utilize redundant storage systems to prevent data loss.

**Monitoring & Observability:**
- **Logging:** Centralized logging (e.g., ELK stack, Splunk) for system events, crawler activities, and submission logs.
- **Metrics & Alerts:** Use Prometheus or Grafana for resource utilization, system performance, and anomaly detection.
- **ML Model Retraining:** Periodic retraining of ML models ensures they stay effective as target ecosystems evolve.

---

## Conclusion

The Data Intelligence Platform brings together advanced crawling, indexing, searching, and whistleblowing tools to form a cohesive intelligence environment. Active Intelligence components proactively harvest and structure hidden data, while Passive Intelligence avenues allow secure, anonymous submissions of insider information.

This integrated approach enables researchers, journalists, OSINT professionals, and security analysts to combine large-scale automated collection with carefully curated whistleblower insights. By continuously refining crawler logic, expanding the set of scraping scripts, and leveraging secure anonymized submissions, the platform remains a powerful, adaptable solution for modern intelligence gathering and analysis.
