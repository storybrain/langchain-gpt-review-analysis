# LangChain-GPT Review Analysis

A repository that demonstrates the integration of LangChain and GPT-3 to extract and analyze reviews and product specifications.

## Overview

This repository contains Jupyter Notebooks that illustrate how to:

- Extract product reviews from web pages using LangChain and analyze them with GPT-3.
- Extract product specifications from given description texts.

In addition, the `code` folder contains example `.py` scripts showcasing different functionalities.

## Contents

1. **Notebooks**:

   - `langchain-gpt-review-analysis.ipynb`: This notebook showcases how to scrape product reviews from Amazon and process them using GPT.
   - `product-specs-extraction.ipynb`: This notebook demonstrates extracting product specifications from description.

2. **Code Folder**:
   - Contains example `.py` scripts illustrating various functionalities.

## Getting Started

1. **Setup Conda Environment**:

   ```bash
   conda create --name langchain python=3.10
   conda activate langchain
   ```

2. **Install Required Libraries**:

   ```bash
   conda install langchain openai asyncio nest_asyncio lxml python-dotenv playwright
   ```

3. **Launch Jupyter Notebook**:

   ```bash
   jupyter notebook
   ```

4. Navigate to the desired notebook and run it.

## Requirements

- A Conda environment with Python 3.9 or later.
- Required libraries: `langchain`, `openai`, `asyncio`, `nest_asyncio`, `lxml`, `python-dotenv`, and `playwright`.

## License

[MIT License](LICENSE)

---

**Note**: The `[MIT License](LICENSE)` link assumes you've included the MIT License in a file named `LICENSE` in the root of your repository. Modify the license section if you're using a different one. Ensure that the Conda environment is set up with the correct version of Python and that the libraries are available for installation via Conda.
