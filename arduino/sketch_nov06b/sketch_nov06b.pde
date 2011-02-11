// LED connected to digital pin 13
int LED_PIN = 11;

void setup() {
  // sets the digital pin as output 
  pinMode(LED_PIN, OUTPUT); 
} 

int v;
void loop() { 
  // sets the LED on 
  v = analogRead(0);
  v += 0;
  v /= 100;
  delay(v);
  analogWrite(LED_PIN, 255);
  delay(v);
  analogWrite(LED_PIN, 0);
  //delay(100);
  /*
  // sets the LED off
  analogWrite(LED_PIN, 1023);
  delay(1000);
  */
}
