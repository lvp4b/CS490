#include <DHT.h>
#include <LiquidCrystal.h>
#include <RestClient.h>

RestClient rest = RestClient("api.thingspeak.com", 443);

// pins
const int dhtp = 23, rs = 22, en = 21, 
  d0 = 19, d1 = 18, d2 = 14, d3 = 26,
  d4 = 27, d5 = 12, d6 = 13, d7 = 15;
  
DHT dht(dhtp, DHT11);
LiquidCrystal lcd(rs, en, d0, d1, d2, d3, d4, d5, d6, d7);

void setup()
{
    dht.begin();
    lcd.begin(16, 2);

    lcd.setCursor(0, 0);
    lcd.print("Connecting...");
    rest.begin("Enter network name", "Enter network password");

    lcd.setCursor(0, 0);
    lcd.print("Connected!");
    delay(1000);
}

void loop()
{    
    // Read sensors
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature() * 9.0f / 5 + 32;
    
    // Print to LCD
    lcd.setCursor(0, 0);
    lcd.print("Humidity:");
    lcd.print(humidity);
    lcd.print("%");

    lcd.setCursor(0, 1);
    lcd.print("Temp:");
    lcd.print(temperature);
    lcd.print(" F");

    // Upload to the internet
    // Enter url with API key
    String url = "/update?api_key=(Enter API Key)&field1=";
    url += humidity;
    url += "&field2=";
    url += temperature;
    int statusCode = rest.get(url.c_str());

    if (statusCode != 200) {
      delay(1000);
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Error: ");
      lcd.print(statusCode);
      delay(1000);
    } else {
      delay(2000);
    }
}
