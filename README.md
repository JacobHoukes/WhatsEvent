# 📢 About our project  

This repository is a result of collaborative work by five students. Our goal was to create a WhatsApp chatbot that provides weather data for a user-selected location and time without leaving WhatsApp.  

In the same workflow, the chatbot suggests events in the chosen location. This eliminates the need to browse event booking websites separately, making group planning much easier. Users can share event results effortlessly with their friends in the chat app without requiring technical knowledge.  

Currently, this is an MVP version, but future enhancements, including AI-powered chatbot responses, are planned.  

### 🌟 Benefits:  
✅ **Seamless**: No need to switch between apps.  
✅ **User-friendly**: Works for people of all ages and backgrounds.  
✅ **Business-friendly**: Helps event organizers reach more customers.  

---  

# ⚙️ Technical Information  

The app runs on the **Twilio API** for WhatsApp communication.  
Weather data is fetched from **WeatherAPI.com**.  
Event data comes from **Ticketmaster API**.  

**To use this project, you must register for these APIs and store your credentials in a `.env` file.**  

---  

# 🚀 Installation & Setup  

### Prerequisites:  
- Python 3.x  
- Virtual environment (optional but recommended)  
- API keys from Twilio, WeatherAPI, and Ticketmaster  

### Setup Steps:  
1. Clone the repository:  
   ```sh
   git clone https://github.com/your-username/WhatsEvent.git
   cd WhatsEvent
   ```  
2. Install dependencies:  
   ```sh
   pip install -r requirements.txt
   ```  
3. Create a `.env` file and add your API keys:  
   ```ini
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   WEATHER_API_KEY=your_weatherapi_key
   TICKETMASTER_API_KEY=your_ticketmaster_key
   ```  
4. Run the application:  
   ```sh
   python main.py
   ```  

---  

# 🔍 Example Usage  

### **Chatbot welcomes user:** 

### **User inputs required info:**  
> "Berlin, YYYY MM DD, HH"  

### **Chatbot Response:**  
🌤 **Weather in Berlin at 18:00:**  
- Temperature: 15°C  
- Condition: Partly Cloudy  

🎭 **Suggested events in Berlin:**  
- 🎸 Rock Concert at "Berlin Arena"  
- 🎭 Theatre Play "Hamlet" at "Berlin Theatre"  

### **User clicks on links to events or forwards message to friends**  

---  

# 📌 Further Requirements  

Our App is built with Python and uses the following libraries:  
- `requests`  
- `os`  
- `dotenv`  
- `json`  
- `twilio.rest`  

To install them manually, run:  
```sh
pip install requests python-dotenv twilio
```

---  

# 🛠️ Future Plans  
🚀 **Planned Enhancements:**  
- AI-powered chatbot responses  
- Support for more event platforms  
- Voice command functionality  

---  

# 🤝 Contributing  

We welcome contributions! If you'd like to improve this project, feel free to fork the repo and create a pull request.  

---  

# 📜 License  

This project is licensed under the **MIT License**. You are free to use, modify, and distribute it. See the [LICENSE](LICENSE) file for more details.  

---  

# 📬 Contact  

Have any questions? Feel free to reach out to us via GitHub Issues or email.  
