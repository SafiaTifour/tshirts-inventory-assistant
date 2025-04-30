# T-shirt inventory SQL Assistant

A natural language interface for querying the AtliQ T-Shirts inventory database. This application allows users to ask questions about the inventory in plain English and receive answers based on SQL queries executed against the database.
Idea: @codebasics

## Features

- **Natural Language Interface:** Ask questions in plain English about the t-shirt inventory
- **SQL Query Generation:** Automatically translates questions into SQL queries
- **Similar Examples:** Shows examples similar to your question to improve understanding
- **Visual Results:** Displays query results in a friendly tabular format
- **Natural Language Answers:** Provides straightforward answers to your questions

## Architecture

The application follows a modular design with clear separation of concerns:

- **Config Module:** Manages application settings and configurations
- **Database Module:** Handles database connections and query execution
- **Model Module:**
  - **LLM Service:** Manages interactions with the Google Gemini API
  - **Vector Store:** Handles example storage and similarity search
  - **Query Generator:** Generates SQL queries from natural language
  - **Answer Generator:** Creates natural language answers from query results
- **Streamlit Interface:** Provides a user-friendly web interface

## Installation

### Prerequisites

- Python 3.9+
- MySQL database with the AtliQ T-Shirts schema
- Google Generative AI API key

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/SafiaTifour/tshirts-inventory-assistant.git
   cd tshirts-inventory-assistant
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the application:
   - Update `config/config.yaml` directly with your settings

## Usage

1. Start the Streamlit app:
   ```bash
   streamlit run main.py
   ```

2. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Type your question in the input field and get answers about the t-shirt inventory!

## Example Questions

- How many white Levi's t-shirts do we have?
- What's the total value of all XL t-shirts in stock?
- Which brand has the highest stock value?
- How many red Nike t-shirts in size M do we have left?
- If we sell all Adidas t-shirts with discounts applied, how much revenue will we generate?

## Database Schema

The application expects a MySQL database named `atliq_tshirts` with the following schema:

- Table: `t_shirts`
  - `t_shirt_id`: Unique ID for each t-shirt
  - `brand`: T-shirt brand (Nike, Adidas, Levi, etc.)
  - `color`: T-shirt color
  - `size`: T-shirt size (XS, S, M, L, XL, etc.)
  - `price`: Unit price
  - `stock_quantity`: Number of items in stock

- Table: `discounts`
  - `t_shirt_id`: Foreign key referencing t_shirts
  - `pct_discount`: Percentage discount applied

