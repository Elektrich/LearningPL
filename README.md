README: Telegram Bot for Learning Python
📌 Project Description
This Telegram bot was created as a final project for a 9th-grade computer science class. The bot provides educational materials on the Python programming language, including text, images, and links to additional resources. The project is developed in Python using the python-telegram-bot library and SQLite for database management.

🌟 Key Features
Educational Material Selection: Users can choose chapters and topics to study.

Content Parsing: The bot extracts text and images from web pages.

User-Friendly Navigation: Buttons for deleting messages and navigating between topics.

Formatting Support: Text is sent with HTML markup for better readability.

🛠 Technologies and Tools
Programming Language: Python

Libraries:

python-telegram-bot — for interacting with the Telegram API.

sqlite3 — for database operations.

requests and BeautifulSoup — for web scraping.

html — for escaping special characters.

Development Environment: PyCharm

Database: SQLite

📂 Project Structure
Copy
.
├── main.py            # Bot core: command and message handling
├── dbwork.py          # Database operations
├── parsework.py       # Parsing educational content
├── config.py          # Configuration data (e.g., bot token)
└── README.md          # Usage instructions
🚀 Installation and Setup
Clone the Repository:

bash
Copy
git clone https://github.com/your-username/your-repository.git
cd your-repository
Install Dependencies:

bash
Copy
pip install python-telegram-bot requests beautifulsoup4
Configure the Bot Token:

Create a bot via BotFather and obtain the token.

Save the token in config.py:

python
Copy
TOKEN = "your-token-here"
Run the Bot:

bash
Copy
python main.py
💡 Usage Examples
Start Command:

The user sends /start, and the bot responds with a welcome message and topic selection options.

Topic Selection:

The bot displays a list of chapters and topics with navigation buttons.

Message Deletion:

Users can delete all messages in a topic by clicking the "Delete All" button.

🐛 Common Issues and Solutions
Error can't parse entities: Caused by improper text formatting. Solution: Use HTML markup.

Error message too long: Text exceeds Telegram's 4096-character limit. Solution: Split the text into smaller parts.

Image Issues: Ensure image URLs are correct and complete.

📈 Future Enhancements
Add support for other programming languages.

Include video and audio materials.

Integrate APIs for automatic content updates.

Implement usage statistics collection.

📚 References
Geek Brains — What is a Chatbot?

Mailfit — Chatbots in Marketing

Habr — Evolution of Chatbots

✉️ Contact
Author: Mark Nesterov, 9th-grade student.

Project Supervisor: Yulia Barybina, Computer Science Teacher.

© 2024-2025 Academic Year, MBOU Secondary School, Korfovsky
