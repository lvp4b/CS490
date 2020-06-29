#include <DHT.h>
#include <LiquidCrystal.h>
#include <RestClient.h>
#include <WiFiUdp.h>
#include <BluetoothSerial.h>

RestClient rest = RestClient("api.thingspeak.com", 443);
RestClient ada = RestClient("io.adafruit.com", 443);
BluetoothSerial bluetooth;

// pins
const int dhtp = 23, rs = 22, en = 21, 
  d0 = 19, d1 = 18, d2 = 14, d3 = 26,
  d4 = 27, d5 = 12, d6 = 13, d7 = 15,
  mhq = 35;
  
DHT dht(dhtp, DHT11);
LiquidCrystal lcd(rs, en, d0, d1, d2, d3, d4, d5, d6, d7);
WiFiUDP udp;

float r0;

void setup()
{
    bluetooth.begin("ESP32test");
    dht.begin();
    lcd.begin(16, 2);

    lcd.setCursor(0, 0);
    lcd.print("Connecting...");
    rest.begin("<my wifi>", "<my wifi password>");

    lcd.setCursor(0, 0);
    lcd.print("Connected!");
    delay(1000);
    r0 = readMhqOverLongTime();
}

float readMhqOverLongTime() {
    float result = 0;
    for(int i = 0; i < 10; i++) {
        result += readMhq();
        delay(100);
    }
    return result / 10;
}

float readMhq() {
    float result = 0;
    for(int i = 0; i < 4; i++) {
        result += analogRead(mhq);
    }
    return 4 / result;
}

// provides a rough PPM concentration of an arbitrary gas
float readMhqRoughPpm() {
    float rsro = readMhq() / r0;
    return exp(-3.227 * log(rsro) + 1.984);
}

float humidity, temperature, gasPpm;
void readSensors() {
    humidity = dht.readHumidity();
    temperature = dht.readTemperature() * 9.0f / 5 + 32;
    gasPpm = readMhqRoughPpm();
}


// increase user satisfaction by updating the LCD more frequently
void updateLcd() {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("MHQ:");
    lcd.print(gasPpm);
    lcd.print(" PPM");

    lcd.setCursor(0, 1);
    // Display levels of health concern
    if (gasPpm >= 0 && gasPpm <= 50) {
        lcd.print("Good");
    } else if (gasPpm >= 51 && gasPpm <= 100) {
        lcd.print("Moderate");
    } else if (gasPpm >= 100 && gasPpm <= 151) {
        lcd.print("Unhealthy for SG");
    } else if (gasPpm >= 151 && gasPpm <= 200) {
        lcd.print("Unhealthy");
    } else if (gasPpm >= 201 && gasPpm <= 300) {
        lcd.print("Very Unhealthy");
    } else {
        lcd.print("Hazardous");
    }
}

void updateBluetooth() {
    unsigned short sGas = (unsigned short)gasPpm;
    bluetooth.write(sGas & 0xFF);
    bluetooth.write((sGas >> 8) & 0xFF);
    bluetooth.flush();
}

// update LCD at high frequency while waiting for the specified delay
void delayUpdateLcd(int ms) {
    unsigned long start = millis();
    do {
        readSensors();
        updateLcd();
        updateBluetooth();
        delay(100);
    } while (millis() - start < ms);
}

void loop()
{
    readSensors();
    updateLcd();

    // Upload to the internet
    String url = "/update?api_key=<my api key>&field1=";
    url += humidity;
    url += "&field2=";
    url += temperature;
    url += "&field3=";
    url += gasPpm;
    int statusCode = rest.get(url.c_str());
 
    if (statusCode != 200 && statusCode != 0) {
        delayUpdateLcd(500);
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("TS Error: ");
        lcd.print(statusCode);
        delay(500);
    } else {
        delayUpdateLcd(1000);
    }

    String buffer = "";
    buffer += humidity;
    buffer += ",";
    buffer += temperature;
    buffer += ",";
    buffer += gasPpm;
    udp.beginPacket("rpi-lia", 25565);
    udp.write((byte*)buffer.c_str(), buffer.length());
    udp.endPacket();
}
