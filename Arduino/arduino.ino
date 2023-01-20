int ledPin = 13;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
}


void loop() {
  if ( Serial.available() > 0 ) {
    int open = Serial.parseInt();
    
    if (open == 1) {
      digitalWrite(ledPin, HIGH);      
      delay(5000);
      digitalWrite(ledPin, LOW);
      Serial.write("0\n");  //Door Locked
      delay(1000);
    }
  }
  delay(50);
}