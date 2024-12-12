# redesigned-personal-assistant
A voice-controlled assistant named "Wolverine," capable of performing various tasks like setting reminders, providing weather updates, playing music, browsing the web, handling system operations, and more, based on user commands.

The script is a voice-controlled assistant named "Wolverine" that performs a variety of tasks based on voice commands. 

Here's a full description of all the functions it can handle:

1. Greeting and Personalization
Wish User: It greets the user with a personalized message based on the time of day (Good Morning, Good Afternoon, or Good Evening).
Introduce Itself: It introduces itself as "Wolverine" and asks how it can help.

3. Voice Commands and Speech Recognition
Take Commands: It listens for voice commands and processes them using speech recognition. If no microphone is found, it asks for input through text.
Speech to Text: It converts speech to text and acts on the commands accordingly.
Handle Queries: It interprets and executes a wide range of user queries.

5. Reminders
Set Reminders: It allows the user to set reminders by specifying a task and a time. The reminder will trigger at the given time.
Check Reminders: It checks the current time and reminds the user of any tasks set previously.

7. Weather Updates
Check Weather: It can provide the current weather details for a given location by fetching data from the OpenWeatherMap API (temperature, weather description, humidity, wind speed, etc.).

9. Web and Online Activities
Wikipedia Search: It can search Wikipedia for information on a given topic and summarize the results.
Google Search: It can search for queries on Google and read the results aloud.
Open Websites: It can open websites like YouTube, Google, Instagram, etc., by voice command.
News Updates: It fetches the latest news headlines from "The Hindu" news site and reads them out loud.

11. Entertainment and Fun
Tell Jokes: It can tell jokes using the pyjokes library to add humor.
Trivia Game: It offers a trivia quiz game, asking random multiple-choice questions and scoring the user based on their responses.
Motivational Quotes: It can fetch and read inspirational quotes using an external quote library.

13. File Management
Open Files: It can open files specified by the user.
Rename Files: It can rename files based on user input.
Move Files: It can move files from one location to another.
Delete Files: It can delete files as per the user’s command.

15. System Operations
Shutdown the System: It can shut down the computer after a 5-second delay.
Restart the System: It can restart the computer after a 5-second delay.
Sleep the System: It can put the system into sleep mode.

17. Voice Control
Change Voice: It can change the voice to male or female based on user preference using pyttsx3 voice engine.

19. Motion Tracking
Track Motion: Using the computer’s webcam, it can track motion and display the movement on the screen. It uses OpenCV to detect motion and draw bounding boxes around the moving object.

21. Calculation
Voice Calculator: It can perform basic arithmetic calculations such as addition, subtraction, multiplication, and division using voice commands (e.g., "add 5 and 3").

23. Translation
Translate Text: It can translate a user-provided phrase into any target language using the Google Translate API.

25. File System Interactions
Open Files: It can open files from the local system.
Rename Files: It can rename a file based on user input.
Move Files: It can move files from one location to another.
Delete Files: It can delete files from the system.

27. Shutdown/Exit
Goodbye: It can terminate the assistant with a "Goodbye" message.

29. Error Handling
Fallback for Unrecognized Queries: If it doesn't understand a query, it tries to look for information on Wikipedia or asks the user to try again.

31. Miscellaneous Features
Track User’s Location: It can track motion using the camera.
Play Music: It can play music from a specified directory (e.g., D:/music) if the directory and files exist.
This script covers a wide range of tasks from information gathering (weather, Wikipedia, news) to file management (open, rename, move, delete) and entertainment (trivia, jokes, motivational quotes). It also handles system operations and provides an interactive, voice-based user experience.

