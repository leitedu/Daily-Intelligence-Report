# Daily-Intelligence-Report

![Status](https://img.shields.io/badge/Status-Archived-inactive?style=for-the-badge)

> 📦 **Project Status:** This repository contains an internal tool that was successfully deployed in a production environment to sturcture and automate PDF report generation. The project is currently in a archived state with no active maintenance planned. Feel free to explore the code.
>
> * **Next Iteration:** Check out the original project at [Market intelligence report update]([https://github.com/seu-usuario/outro-projeto](https://github.com/leitedu/web-scraping/tree/main/Market%20intelligence%20report%20update))

## 📌 Overview

The main objective of this project was to convert the daily creation of a Market Intelligence Report and replaces PowerPoint editing with a PDF generation pipeline. 

Additionally, the project aims to expand Python usage, transition from script-based programming to a modular structure, and replace Excel and VBA processes.



## 🏗️ Architecture & Project Structure

The project follows a modular design pattern, separating data ingestion, processing, visual layout, and pipeline orchestration:

* **`orchestrator.py`**: The entry point of the application. Coordinates the execution flow across data retrieval, transformation, and document rendering.
* **`data.py` & `load.py`**: Responsible for data fetching/ingestion from external web sources and databases.
* **`transform.py`**: Handles data cleaning, formatting, and mathematical calculations required for report metrics.
* **`layout.py` & `header.py`**: Define global visual styling, page setups, typography, and standard headers/footers for the PDF output.
* **`sections.py` & `report.py`**: Assemble dynamic content components into cohesive report sections and compile the final PDF document.
* **`env.example`**: Template for required environment variables (credentials, API endpoints, file paths).



## 🛠️ Key Technologies & Concepts

* **Python 3**
* **ETL Pipeline Design:** Clean separation between Extract (`data.py`), Transform (`transform.py`), and Load (`report.py`).
* **Document Generation:** Programmatic layout rendering and PDF styling.
* **Orchestration:** Automated execution workflow.
