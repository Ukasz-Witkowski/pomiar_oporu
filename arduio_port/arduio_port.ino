int moc = 0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(4, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) 
  {
    String input = Serial.readStringUntil('\n');
    moc=input.toInt();
    Serial.println("zmiana na:");
    Serial.println(moc);
    Serial.flush();
  }
  digitalWrite(LED_BUILTIN, HIGH);
  digitalWrite(4, HIGH);
  delay(10*moc);                       
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(4, LOW);
  delay(10*(100-moc));   
  Serial.println(moc);
 
}
