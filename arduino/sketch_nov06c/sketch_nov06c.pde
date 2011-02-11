int v;

void setup() {
}
void loop() {
  v++;
  digitalWrite(11+(v-v/3*3), HIGH);
  delay(50);
  digitalWrite(11+(v-v/3*3), LOW);
  delay(50);
}
