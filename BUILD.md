Below is an example of a BUILD.md file that explains how to pull down the repository, set up your environment from scratch, and run the interpreter. Save this as `BUILD.md` in your project.

---

# MordorLang Build and Setup Instructions

This document provides step-by-step instructions on how to clone the repository, set up your environment, and run the MordorLang interpreter. These instructions assume nothing about your end-user environment.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Git:** To clone the repository.  
- **Python 3.8 or later:** MordorLang is implemented in Python.  
- **Docker (Optional):** If you prefer to run the project in a container.

## Cloning the Repository

1. **Open a Terminal:**  
   Use Command Prompt, PowerShell (on Windows), or a terminal emulator (on macOS/Linux).

2. **Clone the Repo:**  
   ```bash
   git clone https://github.com/BriScanlon/mordorlang.git
   ```

3. **Change Directory:**  
   Navigate into the cloned repository folder.
   ```bash
   cd mordorlang
   ```

## Setting Up Your Python Environment

### Option 1: Using a Virtual Environment (Recommended)

1. **Create a Virtual Environment:**  
   Run the following command:
   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment:**  
   - **On Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **On macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies:**  
   If a `requirements.txt` file is provided, install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   If no such file exists, ensure any required dependencies for running Python scripts are installed.

### Option 2: Using System Python

Make sure your system has Python 3.8 or later properly installed. Then, you can run the interpreter directly without a virtual environment.

## Running MordorLang

### Running an Example File

Assume you have an example file (e.g., `function_test.mordor`) inside an `examples` directory. Run the interpreter by executing:

```bash
python main.py examples/function_test.mordor
```

### Running in REPL Mode (if supported)

If your interpreter supports an interactive REPL mode, simply run:

```bash
python main.py
```

## Troubleshooting

- **Python Version:** Verify you are using Python 3.8+:
  ```bash
  python --version
  ```

- **Virtual Environment:** Ensure you activate your virtual environment before installing dependencies or running the interpreter.

- **Dependency Errors:** If you encounter missing module errors, check the repository documentation or the `requirements.txt` file (if provided) for additional dependencies.

