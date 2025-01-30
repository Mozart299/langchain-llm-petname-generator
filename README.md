# 🐾 Perfect Pet Name Generator

A delightful Streamlit application that helps pet owners find the perfect name for their furry, feathered, or scaly friends using AI-powered suggestions. The app generates personalized pet names based on your pet's type, color, and personality traits, complete with explanations, fun facts, and suggested nicknames.

## ✨ Features

### Core Functionality
- AI-powered name generation based on pet characteristics
- Personalized suggestions considering pet type, color, and personality
- Detailed explanations for each generated name
- Fun facts and nickname suggestions
- Adjustable creativity levels for name generation

### User Experience
- Clean, intuitive interface with emoji-enhanced navigation
- Multi-tab layout for easy access to different features
- Interactive name gallery
- Favorites system for saving preferred names
- Session history tracking
- Share functionality for social media

### Customization Options
- Multiple pet types with custom options
- Various color selections
- Personality trait selection
- Name style preferences
- Adjustable creativity levels

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Git (optional)

### Setup Steps

1. Clone the repository (or download the source code):
```bash
git clone https://github.com/Mozart299/langchain-llm-petname-generator.git
cd langchain-llm-petname-generator
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root directory:
```bash
OPENAI_API_KEY=your_api_key_here
```

## 📖 Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Navigate to the application in your web browser (typically `http://localhost:8501`)

3. Generate a pet name:
   - Select or enter your pet type
   - Choose or specify your pet's color
   - (Optional) Select personality traits
   - Adjust the creativity level
   - Click "Generate Perfect Name"

4. Manage your generated names:
   - Save favorites for later reference
   - View your name history
   - Share names you like
   - Copy generated names to clipboard

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Customization Options
- Adjust the creativity level (0.0 to 1.0)
- Select name style preferences
- Modify personality traits list
- Customize pet types and colors

## 📁 Project Structure

```
pet-name-generator/
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── .env               # Environment variables
├── README.md          # Project documentation
└── .gitignore         # Git ignore file
```

## 💻 Development

### Requirements File (requirements.txt)
```
streamlit
langchain-openai
python-dotenv
```

### Contributing
1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a pull request

## 🔒 Security

- Never commit your `.env` file
- Keep your OpenAI API key secure
- Regularly update dependencies
- Monitor API usage

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your OpenAI API key is correctly set in the `.env` file
   - Verify the `.env` file is in the correct directory

2. **Package Installation Issues**
   - Try upgrading pip: `pip install --upgrade pip`
   - Install packages one by one to identify problematic dependencies

3. **Streamlit Connection Error**
   - Check if port 8501 is available
   - Verify network connectivity
   - Try restarting the application

### Getting Help
- Check the existing issues on GitHub
- Create a new issue with detailed information about your problem
- Include error messages and steps to reproduce the issue

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for providing the API
- Streamlit for the excellent web framework
- The open-source community for various dependencies

## 🔄 Version History

### v1.0.0 (Initial Release)
- Basic name generation functionality
- User interface with Streamlit
- Favorites and history features
- Sharing capabilities

## 📧 Contact

For support or queries:
- Create an issue on GitHub
- Contact the maintainer at [your-email]
- Join our community Discord [optional]

## 🗺️ Roadmap

### Planned Features
- Multiple language support
- Custom theme options
- Name popularity statistics
- Integration with pet name databases
- Export functionality for name history
- Mobile app version

### Under Consideration
- Machine learning model for personalized suggestions
- Community voting system
- Integration with social media platforms
- Premium features for advanced users

---
Made with ❤️ for pet owners everywhere
