# wotb-chatbot

## Overview

This porjects is a

### Features

- **Asynchronous MongoDB operations** using Motor.
- **OpenAI GPT integration** for enhanced conversation capabilities.
- **Customizable prompts** for various use cases.
- **Built-in error handling** for robust production usage.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.9+
- MongoDB
- OpenAI API Key

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/wotb-chatbot.git
   cd wotb-chatbot
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your `.env` file with your MongoDB URI and OpenAI API key.

## Usage

1. Run the chatbot:

   ```
   bash
   python3 console_app/ __main__.py

   ```

2. To interact with the chatbot through the terminal, choose option 9. ChatGPT can answer question about the band Wake of the Blade's shows based on the data in thw Wake of the Blade database with the helper functions in the mongo directory.

## Configuration

- Customize chatbot behavior by modifying the prompts in `openai_custom/utils.py`.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-branch`).
3. Make your changes and test them thoroughly.
4. Submit a pull request for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
