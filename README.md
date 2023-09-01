# EPFL Restaurant Menu Scraper

This project is a Python script for scraping and updating daily menus from EPFL campus restaurants. It uses web scraping techniques to extract menu information (prices, vegetarian, ...) and stores it in a CSV file. Additionally, it provides a GitHub Actions workflow (cron job) to automate the scraping and updating process daily.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [GitHub Actions Workflow](#github-actions-workflow)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

You can install the required packages using the following command:

```bash
pip install -r requirements.txt
```

## Project Structure

The project consists of the following main components:

- **utils.py**: Contains Python functions for scraping EPFL restaurant menus and saving them in a CSV file.

- **cron.py**: A script that runs daily to scrape the menu for the current date and appends it to the existing CSV file.

- **scrap_all.py**: A script that scrapes menus between two dates and appends them to the existing CSV file.

- **cron_scrap.yaml**: GitHub Actions workflow file that schedules the `cron.py` script to run daily at a specific time.

- **data/menus.csv**: The CSV file where menu data is stored.

## Usage

1. Clone this repository to your local machine.

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the `cron.py` script to scrape and update the menu for the current date:

   ```bash
   python cron.py
   ```

   This script will check if the menu for the current date is already in the CSV file. If not, it will scrape the menu and append it to the CSV file.

4. You can also run the `scrap_all.py` script to scrape menus between two dates (change the `start_date` and `end_date` variables in the script):

   ```bash
   python scrap_all.py
   ```

   This script will scrape the menus for all dates between `start_date` and `end_date` and append them to the CSV file if they are not already there.

## GitHub Actions Workflow

This project includes a GitHub Actions workflow that automates the menu scraping process daily. The workflow is scheduled to run at 00:00 UTC (2:00 UTC+2) (adjust the cron schedule in `cron_scrap.yaml` if needed).

When the workflow runs, it performs the following steps:

1. Checks out the repository content.

2. Sets up the Python environment and installs the required packages.

3. Executes the `cron.py` script to scrape and update the menu for the current date.

4. Commits any changes made during the update to the GitHub repository.

5. Pushes the changes back to the repository.

This ensures that the menu data is automatically updated every day without manual intervention.

## Contributing

Contributions to this project are welcome. If you have any suggestions, bug fixes, or improvements, please open an issue or create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.