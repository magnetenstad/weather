from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import re

class Forecast:
  def __init__(self, place, day, temp, rain, wind):
    self.place = place
    self.day = day
    self.temp = temp
    self.rain = rain
    self.wind = wind

  def print(self, forecasts):
    emojis = ""
    if self.temp == max([forecast.temp for forecast in forecasts]):
      emojis += "🥵"
    if self.temp == min([forecast.temp for forecast in forecasts]):
      emojis += "🥶"
    if self.rain == max([forecast.rain for forecast in forecasts]):
      emojis += "🌧️"
    if self.rain == min([forecast.rain for forecast in forecasts]):
      emojis += "🌤️"
    if self.wind == max([forecast.wind for forecast in forecasts]):
      emojis += "💨"
    if self.wind == min([forecast.wind for forecast in forecasts]):
      emojis += "〰️"

    print(f"{(self.place + ' '*10)[:6]}\t🌡️  {self.temp:.2f}\t🌧️  {self.rain:.2f}\t💨 {self.wind:.2f}\t{emojis}")
    
def get_int(text):
  try:
    return int("".join(
      [char if char.isnumeric() else "" for char in text]))
  except:
    return 0 

def get_float(text):
  try:
    return float("".join(
      [char if re.match("([0-9]|\.|\,)", char) else "" for char in text]
      ).replace(",", "."))
  except:
    return 0 

def get_latlng(text):
  return [get_float(value) for value in text.split(",")] 

def avg(array):
  return sum(array) / len(array)

def get_forecast(driver, place, latlng, day, dayIndex):
  driver.get(f"https://www.yr.no/nb/v%C3%A6rvarsel/timetabell/{latlng[0]},{latlng[1]}/?i={dayIndex}")

  WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "fluid-table__row")))
  rows = driver.find_elements(By.CLASS_NAME, "fluid-table__row")

  temp_avg = avg([get_int(row.find_element(
    By.CLASS_NAME, "temperature").text) for row in rows])
  rain_values = []
  for row in rows:
    els = row.find_elements(By.CLASS_NAME, "precipitation__value")
    for el in els:
      rain_values.append(get_float(el.text))
    for _ in range(2 - len(els)):
      rain_values.append(0)
  rain_avg = avg(rain_values)
  wind_avg = avg([get_int(row.find_element(
    By.CLASS_NAME, "wind__value").text) for row in rows])
  return Forecast(place, day, temp_avg, rain_avg, wind_avg)

if __name__ == "__main__":
    
  places = {
    "Rjukan": "59.8792° N, 8.6117° E",
    "Odda": "59.9373° N, 6.9177° E",
    "Vaset": "60.9874° N, 8.9678° E",
    "Flåm": "60.8608° N, 7.1118° E",
    "Loen": "61.8711° N, 6.8480° E",
    "Geiranger": "62.1015° N, 7.0941° E",
    "Åndalsnes": "62.5674° N, 7.6872° E",
    "Kårvåg": "63.0138° N, 7.4474° E",
    "Kristiansund": "63.1103° N, 7.7281° E",
    "Leikanger": "61.1859° N, 6.8080° E",
    "Ålesund": "62.4722° N, 6.1495° E",
    "Lom": "61.8384° N, 8.5666° E",
    "Otta": "61.7732° N, 9.5390° E",
  }

  days = {(datetime.today() + timedelta(days=i)).strftime("%A"): i
    for i in range(2, 7)}
    
  driver = webdriver.Chrome("chromedriver.exe")
  for day, day_index in days.items():
    print(f"\n📆 {day}\n")
    forecasts = []
    for place, coords in places.items():
      latlng = get_latlng(coords)
      forecasts.append(get_forecast(driver, place, latlng, day, day_index))
    for forecast in forecasts:
      forecast.print(forecasts)
  driver.quit()
