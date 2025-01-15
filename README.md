Inspired by - `https://github.com/achiit/India_Info`
Here is a `README.md` for your project:

```markdown
# PanchayatDirectory

A web application to manage and access data from the India Local Government Directory. This project includes scripts to extract, process, and manage large CSV files, along with an API to serve the data.

## Installation

To set up the project locally, follow these steps:

### Clone the Repository
```bash
git clone https://github.com/dhruvagrawal27/PanchayatDirectory.git
cd PanchayatDirectory
```

### Set Up a Virtual Environment
Create and activate a Python virtual environment to manage dependencies:
```bash
python -m venv .venv
# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Run the Application
Start the application by running the API script:
```bash
python api.py
```
The application will be accessible at [http://localhost:5000](http://localhost:5000).

## Additional Features

### Extract CSV Data
To extract a CSV file from the India Local Government Directory, run the following command:
```bash
python main.py
```

### Compress Large CSV Files
Due to the 100 MB upload limit on Supabase, the CSV file is compressed by removing some data rows. To compress the file, use:
```bash
python compress.py
```
utions are welcome! Feel free to open issues or submit pull requests to improve the project.
```
