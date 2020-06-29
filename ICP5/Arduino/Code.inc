// Defines pins numbers
const int trigPin = 12;
const int echoPin = 11;
const int ledPin = 9;

void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(ledPin, OUTPUT); // Sets the LED and buzzer on the same pin as an Output
  Serial.begin(115200); // Starts the serial communication
}

void loop() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds, max 2 meters
  long duration = pulseIn(echoPin, HIGH, 11764);

  // Calculating the distance
  float distance= (duration*0.034)/2;  //Speed of sound in air  at  standard condition = 0.034cm/µs
  
  String message = "Distance ";

  if (distance == 0) {
    message += ">200cm";
    digitalWrite(ledPin, LOW);
  } else if (distance < 50) {
    message += distance;
    message += "cm (WARNING!!)";

    // flash LED and make noises
    digitalWrite(ledPin, !digitalRead(9));
  } else {
    message += distance;
    message += "cm";
    digitalWrite(ledPin, LOW);
  }
  
  // Prints the distance on the Serial Monitor
  Serial.println(message);
    
  delay(100);
}
