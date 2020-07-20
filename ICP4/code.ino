#include <Wire.h>
#include <DHT.h>
#include <LiquidCrystal.h>
#include <RestClient.h>
#include <WiFiUdp.h>
#include <BluetoothSerial.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_SI1145.h>
// pins
const int dhtp = 23, rs = 25, en = 33, 
  d0 = 19, d1 = 18, d2 = 14, d3 = 26,
  d4 = 27, d5 = 12, d6 = 13, d7 = 15,
  mhqPin = 35, lightPin = 39;
// 22 = sck - i2c
// 21 = scl - i2c
// I2C devices
// 0x20 - MCP23017 16-pin I/O expander
// 0x60 - Si1145 UV sensor
// 0x77 - BMP280 pressure sensor
const int io = 0x20;
LiquidCrystal lcd(rs, en, d0, d1, d2, d3, d4, d5, d6, d7);
enum LedState {
  GOOD,
  BAD
};
// Manages the red/green LEDs near each sensor
class Leds {
public:
  void reset() {
    for(int i = 0; i != 5; i++){
      states[i] = GOOD;
    }
  }
  void setState(int pin, LedState state) {
    if (states[pin] < state) {
      states[pin] = state;
    }
  }
  void update() {
    byte greens = 0;
    byte reds = 0;
    for(int i = 0; i != 5; i++){
      auto state = states[i];
      switch(state) {
        case GOOD:
          greens = greens | (1 << i);
          break;
        default:
          reds = reds | (1 << i);
          break;
      }
    }
    // write to the output latch register
    Wire.beginTransmission(io);
    Wire.write(0x14);
    Wire.write(greens);
    Wire.write(reds);
    Wire.endTransmission();
  }
  void begin() {
    // set pin mode to output
    Wire.beginTransmission(io);
    Wire.write(0x00);
    Wire.write(0xE0);
    Wire.write(0xE0);
    Wire.endTransmission();
    reset();
    update();
  }
private:
  LedState states[5];
} leds;
// Base class for all types of sensors implemented
class Sensor {
public:
  virtual void begin() {
  }
  // updates the value of this sensor
  void update() {
    value = read();
    leds.setState(ledPin, getLedState());
  }
  virtual void updateLcd() = 0;
  float getValue() {
    float result;
    result = read();
    return result;
  }
  virtual const char* getFeedKey() = 0;
  virtual LedState getLedState() = 0;
protected:
  Sensor(byte ledPin) : ledPin(ledPin) {
  }
  virtual float read() = 0;
  float value;
private:
  byte ledPin;
};
// Air quality (MQ135) sensor
class Mhq : public Sensor {
public:
  Mhq() : Sensor(0) {
  }
  void begin() {
    r0 = readMhqOverLongTime();
  }
  const char* getFeedKey() {
    return "air-feed";
  }
protected:
  float read() {
    // provides a rough PPM concentration of an arbitrary gas
    float rsro = readMhq() / r0;
    return exp(-3.227f * log(rsro) + 1.984f);
  }
  void updateLcd() {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("MHQ: ");
    lcd.print(value);
    lcd.print(" PPM");
    lcd.setCursor(0, 1);
    // Display levels of health concern
    if (value >= 0 && value <= 50) {
        lcd.print("Good");
    } else if (value >= 51 && value <= 100) {
        lcd.print("Moderate");
    } else if (value >= 100 && value <= 151) {
        lcd.print("Unhealthy for SG");
    } else if (value >= 151 && value <= 200) {
        lcd.print("Unhealthy");
    } else if (value >= 201 && value <= 300) {
        lcd.print("Very Unhealthy");
    } else {
        lcd.print("Hazardous");
    }
  }
  LedState getLedState() {
    if (value <= 50) {
      return GOOD;
    } else {
      return BAD;
    }
  }
private:
  float r0;
  float readMhq() {
    float result = 0;
    for(int i = 0; i < 4; i++) {
      result += analogRead(mhqPin);
    }
    return 4 / result;
  }
  float readMhqOverLongTime() {
    float result = 0;
    for(int i = 0; i < 10; i++) {
      result += readMhq();
      delay(100);
    }
    return result / 10;
  }
} mhq;
// Temperature and humidity sensor
class DhtHumidity : public Sensor {
public:
  DhtHumidity(DHT& dht) : Sensor(4), dht(dht) {}
  const char* getFeedKey() {
    return "humidity";
  }
protected:
  float read() {
    return dht.readHumidity();
  }
  void updateLcd() {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Humidity: ");
    lcd.print(value);
    lcd.print("%");
    lcd.setCursor(0, 1);
    if (value < 30) {
      lcd.print("Too dry for noses");
    } else if (value <= 70) {
      lcd.print("Comfortable");
    } else {
      lcd.print("Too moist");
    }
  }
  LedState getLedState() {
    if (value >= 30 && value <= 70) {
      return GOOD;
    } else {
      return BAD;
    }
  }
private:
  DHT& dht;
};
class DhtTemperature : public Sensor {
public:
  DhtTemperature(DHT& dht) : Sensor(4), dht(dht) {}
  const char* getFeedKey() {
    return "temperature";
  }
protected:
  float read() {
    return dht.readTemperature() * 9.0f / 5 + 32;
  }
  void updateLcd() {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Temp.: ");
    lcd.print(value);
    lcd.print("F");
    lcd.setCursor(0, 1);
    if (value < 50) {
      lcd.print("Need a coat");
    } else if (value < 66) {
      lcd.print("It's cold");
    } else if (value <= 74) {
      lcd.print("It's comfortable");
    } else if (value <= 90) {
      lcd.print("It's too warm");
    } else {
      lcd.print("It's too hot!");
    }
  }
  LedState getLedState() {
    if (value >= 66 && value <= 74) {
      return GOOD;
    } else {
      return BAD;
    }
  }
private:
  DHT& dht;
};
// Barometer sensor
class Pressure : public Sensor {
public:
  Pressure() : Sensor(1) {}
  void begin() {
    bmp.begin();
    bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,
                    Adafruit_BMP280::SAMPLING_X2, // temperature
                    Adafruit_BMP280::SAMPLING_X16, // pressure
                    Adafruit_BMP280::FILTER_X16,
                    Adafruit_BMP280::STANDBY_MS_500);
  }
  const char* getFeedKey() {
    return "pressure";
  }
protected:
  float read() {
    return bmp.readPressure() / 100;
  }
  void updateLcd() {
    // Display the pressure value in hectopascals
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Press:");
    lcd.print(value);
    lcd.print(" hPa");
    lcd.setCursor(0, 1);
    if (value >= 1015.8f) {
      lcd.print("Fair weather");
    } else {
      lcd.print("Stormy weather");
    }
  }
  LedState getLedState() {
    if (value >= 1015.8f) {
      // Fair weather
      return GOOD;
    } else {
      // Stormy weather
      return BAD;
    }
  }
private:
  Adafruit_BMP280 bmp;
} pressure;
// UV sensor
class Uv : public Sensor {
public:
  Uv() : Sensor(2) {}
  void begin() {
    uv.begin();
  }
  const char* getFeedKey() {
    return "uv-index";
  }
protected:
  float read() {
    // read UV index
    return uv.readUV() / 100.0f;
  }
  void updateLcd() {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("UV Index: ");
    lcd.print(value);
    // Set threshold for uv index
    lcd.setCursor(0, 1);
    if (value <= 2) {
      lcd.print("Low");
    } else if (value <= 5) {
      lcd.print("Moderate");
    } else if (value <= 7) {
      lcd.print("High");
    } else if (value <= 10) {
      lcd.print("Very High");
    } else {
      lcd.print("Extreme");
    }
  }
  LedState getLedState() {
    if (value < 6) {
      return GOOD;
    } else {
      return BAD;
    }
  }
private:
  Adafruit_SI1145 uv;
} uv;
// Light sensor
class Light : public Sensor {
public:
  Light() : Sensor(3) {}
  const char* getFeedKey() {
    return "light";
  }
protected:
  float read() {
    return analogRead(lightPin) / 40.95f;
  }
  void updateLcd() {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Light: ");
    lcd.print(value);
    lcd.print("%");
    lcd.setCursor(0, 1);
    if (value < 40) {
      lcd.print("It's dark");
    } else {
      lcd.print("There's light!");
    }
  }
  LedState getLedState() {
    if (value >= 40) {
      return GOOD;
    } else {
      return BAD;
    }
  }
} light;
DHT dhtSensor(dhtp, DHT11);
DhtHumidity dhtHumidity(dhtSensor);
DhtTemperature dhtTemperature(dhtSensor);
Sensor* sensors[] = { &pressure, &uv, &mhq, &light, &dhtHumidity, &dhtTemperature };
// Base class for an output where data is uploaded to
class Output {
public:
  virtual void begin() {
  }
  virtual void update() {
    int now = millis();
    if (now - lastTime < getDelay()) {
      // upload every x milliseconds
      return;
    }
    lastTime = now;
    upload();
  }
protected:
  virtual void upload() = 0;
  virtual int getDelay() = 0;
private:
  int lastTime;
};
class Raspberry : public Output {
public:
  Raspberry() : rest("localhost", 443) {}
  void begin() {
    rest.begin("Wifi", "password");
  }
protected:
  void upload() {
    String buffer = "";
    for (int i = 0; i != sizeof(sensors) / sizeof(sensors[0]); i++){
      buffer += sensors[i]->getValue();
      buffer += ",";
    }
    udp.beginPacket("rpi-lia", 25565);
    udp.write((byte*)buffer.c_str(), buffer.length());
    udp.endPacket();
  }
  int getDelay() { return 5000; }
private:
  RestClient rest = RestClient("localhost", 80);
  WiFiUDP udp;
} raspberry;
class LcdOutput : public Output {
protected:
  void upload() {
    index++;
    if (index >= sizeof(sensors) / sizeof(sensors[0])) {
      index = 0;
    }
    sensors[index]->updateLcd();
  }
  int getDelay() { return 2000; }
private:
  int index;
} lcdOutput;
Output* outputs[] = { &lcdOutput, &raspberry };
void setup()
{
  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connecting...");
  for (auto output : outputs) {
    output->begin();
  }
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connected!");
  delay(1000);
  dhtSensor.begin();
  for (auto sensor : sensors) {
    sensor->begin();
  }
  leds.begin();
}
void loop()
{
  leds.reset();
  for (auto sensor : sensors) {
    sensor->update();
  }
  leds.update();
  for (auto output : outputs) {
    output->update();
  }
  delay(50);
}
