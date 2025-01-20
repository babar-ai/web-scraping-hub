# Web Scraping Project: RUC Data Extraction

This project automates the process of extracting data from the SISCOMEX platform using RUC (Registro Único de Comércio) identifiers. It involves web scraping techniques, data processing, and Excel file manipulation to retrieve, process, and save the extracted data.

---

## Features

- **Automated Web Scraping**:
  - Uses `Playwright` to interact with the SISCOMEX platform.
  - Handles dynamic content and potential CAPTCHA challenges.

- **Data Processing**:
  - Extracts and organizes `Data / Hora` and `Evento` information for each RUC.
  - Processes extracted data into a structured format.

- **Excel Integration**:
  - Reads input data from an Excel file (`Teste.xlsx`).
  - Updates and formats the Excel file with extracted and processed data.

---

## Tools & Libraries

This project uses the following tools and libraries:

- **[Playwright](https://playwright.dev/python/)**: For browser automation and web scraping.
- **[pandas](https://pandas.pydata.org/)**: For data manipulation and processing.
- **[openpyxl](https://openpyxl.readthedocs.io/)**: For working with Excel files.
- **[nest_asyncio](https://pypi.org/project/nest-asyncio/)**: To enable nested asynchronous loops.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/web-scraping-project.git
   cd web-scraping-project
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have Playwright browsers installed:
   ```bash
   playwright install
   ```

---

## Usage

1. **Prepare the Input File**:
   - Place an Excel file named `Teste.xlsx` in the project directory.
   - The file should contain a column named `RUC` with identifiers.

2. **Run the Script**:
   Execute the script using:
   ```bash
   python final_finalized.py
   ```

3. **CAPTCHA Handling**:
   - If a CAPTCHA is detected, the script will pause for manual resolution.
   - Solve the CAPTCHA in the browser and press Enter to continue.

4. **Output**:
   - The processed and styled Excel file will be saved as `Teste.xlsx`.

---

## Project Structure

```
web-scraping-project/
├── final_finalized.py      # Main Python script
├── requirements.txt        # Python dependencies
├── Teste.xlsx              # Input file (user-provided)
├── README.md               # Project documentation
```

---

## Known Issues

- CAPTCHA challenges require manual intervention.
- The script assumes the input file contains valid and unique RUCs.

---

## License

This project is licensed under the [MIT License](LICENSE).

---


