import requests
import tkinter as tk
import time
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Call API and return weather data.
def get_weather_from_api(state):
  response = requests.get(f"{BASE_URL}?q={state}&appid={API_KEY}&units=imperial")
  if response.status_code == 200:
    data = response.json()
    tempF = data["main"]["temp"]
    tempMin = data["main"]["temp_min"]
    tempMax = data["main"]["temp_max"]
    humidity = data["main"]["humidity"]
    feelsLike = data["main"]["feels_like"]
    description = data["weather"][0]["description"]
    pressure = data["main"]["pressure"]
    windSpeed = data["wind"]["speed"]
    windGust = data["wind"].get("gust", "No gusts reported")
    return {
      "state": state,
      "temperature": f"{tempF}°F",
      "feels_like": f"{feelsLike}°F",
      "description": description.title(),
      "temp_min": f"{tempMin}°F",
      "temp_max": f"{tempMax}°F",
      "pressure": f"{pressure} hPa",
      "humidity": f"{humidity}%",
      "wind_speed": f"{windSpeed} mph",
      "wind_gust": windGust if windGust != "No gusts reported" else "No gusts",

    }
  else:
    return None




# Read user input, update labels with weather information.
def get_weather():
  state = state_entry.get()
  if not state:
    messagebox.showerror("Error", "Please enter a state name!")
    return

  weather = get_weather_from_api(state)
  if(weather):
    # Update the label with weather details
    t.config(text=weather['temperature'])
    f.config(text=weather['feels_like'])
    d.config(text=weather['description'])
    tmin.config(text=weather['temp_min'])
    tmax.config(text=weather['temp_max'])
    w.config(text=weather['wind_speed'])
    wg.config(text=weather['wind_gust'])
    h.config(text=weather['humidity'])
    p.config(text=weather['pressure'])
    s.config(text=weather['state'])
  else:
    messagebox.showerror("Error,", "State not found. Please try again.")


root = tk.Tk()
root.title("Weather App")
root.geometry("1200x700")
root.resizable(False, False)


# Canvas for background
canvas = tk.Canvas(root, width=1200, height=700)
canvas.pack(fill="both", expand=True)


# Load GIF frames
frames = []
gif = Image.open("weather.gif")
try:
  while True:
    frame = ImageTk.PhotoImage(gif.copy())
    frames.append(frame)
    gif.seek(len(frames))  # Go to the next frame
except EOFError:
  pass  # End of GIF

# Function to animate GIF
current_frame = 0

def animate_gif():
  global current_frame
  canvas.create_image(0, 0, image=frames[current_frame], anchor="nw")
  current_frame = (current_frame + 1) % len(frames)
  root.after(100, animate_gif)  # Adjust the delay for frame rate

animate_gif()



# Add blue box around search bar.
entry_frame = tk.Frame(root, bg="#ADD8E6", padx=30, pady=30)
entry_frame.place(x=400, y=0)

# Input field for the state.
state_entry = ttk.Entry(entry_frame, width=30, font=("Helvetica", 16))
state_entry.pack(ipadx=5, ipady=5)

# Button to get weather.
submit_button = tk.Button(root, text="Get Weather", width=10, height=1, command=get_weather, font=("Helvetica", 12), bg="lightblue", fg="white")
submit_button.place(x=570, y=100)

# Label displaying which state is being observed.
state_label = tk.Label(text="State", font=("Helvetica", 14, "italic"), fg="white", bg="lightblue")
state_label.place(x=570, y=2)

# Labels to display the weather details
label1 = tk.Label(root, text="TEMPERATURE", font=("Helvetica", 12, "bold"), bg="lightgray", fg="white")
label1.place(x=100, y=250)

label2 = tk.Label(root, text="FEELS LIKE", font=("Helvetica", 12, "bold"), bg="lightgray", fg="white")
label2.place(x=400, y=250)

label3 = tk.Label(root, text="DESCRIPTION", font=("Helvetica", 12, "bold"), bg="lightgray", fg="white")
label3.place(x=700, y=250)

label4 = tk.Label(root, text="TEMP MIN", font=("Helvetica", 12, "bold"), bg="lightgray", fg="white")
label4.place(x=1000, y=250)

label5 = tk.Label(root, text="TEMP MAX", font=("Helvetica", 12, "bold"), bg="lightgray", fg="white")
label5.place(x=100, y=400)

label6 = tk.Label(root, text="PRESSURE", font=("Helvetica", 12, "bold"), bg="lightgray", fg="white")
label6.place(x=550, y=550)

label7 = tk.Label(root, text="HUMIDITY", font=("Helvetica", 12, "bold"), bg="lightgray", fg="white")
label7.place(x=1000, y=400)

label8 = tk.Label(root, text="WIND", font=("Helvetica", 12, "bold"), bg="lightgray", fg="white")
label8.place(x=400, y=400)

label9 = tk.Label(root, text="WIND GUSTS", font=("Helvetica", 12, "bold"), bg="lightgray", fg="white")
label9.place(x=700, y=400)

label10 = tk.Label(root, text=f"STATE: ", font=("Helvetica", 20, "bold"), fg="white", bg="lightgray")
label10.place(x=900, y=120)


# Placeholder weather data labels.
s = tk.Label(text="...", font=("arial", 20, "bold"), bg="lightgray", fg="white")
s.place(x=1015,y=120)

t = tk.Label(text="...", font=("arial", 20, "bold"), bg="lightgray", fg="white")
t.place(x=150, y=310, anchor="center")

f = tk.Label(text="...", font=("arial", 20, "bold"), bg="lightgray", fg="white")
f.place(x=430, y=310, anchor="center")

d = tk.Label(text="...", font=("arial", 20, "bold"), bg="lightgray", fg="white")
d.place(x=735, y=310, anchor="center")

tmin = tk.Label(text="...", font=("arial", 20, "bold"), bg="lightgray", fg="white")
tmin.place(x=1020, y=310, anchor="center")

tmax = tk.Label(text="...", font=("arial", 20, "bold"), bg="lightgray", fg="white")
tmax.place(x=125, y=460, anchor="center")

w = tk.Label(text="...", font=("arial", 20, "bold"), bg="lightgray", fg="white")
w.place(x=409, y=460, anchor="center")

wg = tk.Label(text="...", font=("arial", 20, "bold"), bg="lightgray", fg="white")
wg.place(x=733, y=460, anchor="center")

h = tk.Label(text="...", font=("arial", 20, "bold"), bg="lightgray", fg="white")
h.place(x=1020, y=460, anchor="center")

p = tk.Label(text="...", font=("arial", 20, "bold"), bg="lightgray", fg="white")
p.place(x=580, y=610, anchor="center")

# Logo
logo_image = tk.PhotoImage(file='images/weather_icon.png')
logo = tk.Label(image=logo_image, bg="gray")
logo.place(x=85,y=20)

# Run the Tkinter main loop
root.mainloop()
