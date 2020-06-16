void setup() {
  pinMode(1, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, INPUT);
}

void loop() {
  int switchState = digitalRead(4);
  
  if(switchState == LOW) {
  // the button is not pressed

  digitalWrite(1, HIGH); // green LED
  digitalWrite(2, LOW); // red LED
  digitalWrite(3, LOW); // red LED
  }

  else {
  digitalWrite(1, LOW);
  digitalWrite(2, LOW);
  digitalWrite(3, HIGH);

  delay(100); // wait for a 100 seconds
  digitalWrite(2, HIGH);
  digitalWrite(3, LOW);
  delay(100);
  }
}
