// defines pins numbers
const int led1 = 10;
const int led2 = 13;
const int led3 = 9;
const int led4 = 12;
const int led5 = 8;
const int led6 = 11;
String data;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); //initialize serial COM at 9600 baudrate
  
  pinMode(led1, OUTPUT); //make the LED pin as output
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);
  pinMode(led5, OUTPUT);
  pinMode(led6, OUTPUT);
  
  Serial.println("Hi!, I am Arduino");
}

void loop() {
  while (Serial.available()){
    delay(30);
    data = Serial.readString();
    Serial.print("Arduino received: ");
    Serial.println(data);
    delay(500);
  }
//  Serial.print("Arduino received: ");
//  Serial.println(data);
//  delay(500);
  if (data.indexOf("ONE") > -1){
    digitalWrite (led1, HIGH);
    digitalWrite (led2, LOW);
    digitalWrite (led3, LOW);
    digitalWrite (led4, LOW);
    digitalWrite (led5, LOW);
    digitalWrite (led6, LOW);
  }
  else if (data.indexOf("TWO") > -1){
    digitalWrite (led1, HIGH);
    digitalWrite (led2, LOW);
    digitalWrite (led3, HIGH);
    digitalWrite (led4, LOW);
    digitalWrite (led5, LOW);
    digitalWrite (led6, LOW);
  }
  else if (data.indexOf("THREE") > -1){
    digitalWrite (led1, HIGH);
    digitalWrite (led2, HIGH);
    digitalWrite (led3, LOW);
    digitalWrite (led4, LOW);
    digitalWrite (led5, LOW);
    digitalWrite (led6, LOW);
  }
  else if (data.indexOf("FOUR") > -1){
    digitalWrite (led1, HIGH);
    digitalWrite (led2, HIGH);
    digitalWrite (led3, LOW);
    digitalWrite (led4, HIGH);
    digitalWrite (led5, LOW);
    digitalWrite (led6, LOW);
  }
  else if (data.indexOf("FIVE") > -1){
    digitalWrite (led1, HIGH);
    digitalWrite (led2, LOW);
    digitalWrite (led3, LOW);
    digitalWrite (led4, HIGH);
    digitalWrite (led5, LOW);
    digitalWrite (led6, LOW);
  }
  else if (data.indexOf("SIX") > -1){
    digitalWrite (led1, HIGH);
    digitalWrite (led2, HIGH);
    digitalWrite (led3, HIGH);
    digitalWrite (led4, LOW);
    digitalWrite (led5, LOW);
    digitalWrite (led6, LOW);
  }
  else if (data.indexOf("SEVEN") > -1){
    digitalWrite (led1, HIGH);
    digitalWrite (led2, HIGH);
    digitalWrite (led3, HIGH);
    digitalWrite (led4, HIGH);
    digitalWrite (led5, LOW);
    digitalWrite (led6, LOW);
  }
  else if (data.indexOf("EIGHT") > -1){
    digitalWrite (led1, HIGH);
    digitalWrite (led2, LOW);
    digitalWrite (led3, HIGH);
    digitalWrite (led4, HIGH);
    digitalWrite (led5, LOW);
    digitalWrite (led6, LOW);
  }
  else if (data.indexOf("NINE") > -1){
    digitalWrite (led1, LOW);
    digitalWrite (led2, HIGH);
    digitalWrite (led3, HIGH);
    digitalWrite (led4, LOW);
    digitalWrite (led5, LOW);
    digitalWrite (led6, LOW);
  }
  else if (data.indexOf("ZERO") > -1){
    digitalWrite (led1, LOW);
    digitalWrite (led2, HIGH);
    digitalWrite (led3, HIGH);
    digitalWrite (led4, HIGH);
    digitalWrite (led5, LOW);
    digitalWrite (led6, LOW);
  }
  else{ //nothing
    digitalWrite (led1, LOW);
    digitalWrite (led2, LOW);
    digitalWrite (led3, LOW);
    digitalWrite (led4, LOW);
    digitalWrite (led5, LOW);
    digitalWrite (led6, LOW);
  }
}
