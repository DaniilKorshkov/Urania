/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogReadSerial
*/


const int AZERO = A0;
const int RED_PIN = 3;
const int GREEN_PIN = 4;
const int BLUE_PIN = 5;


// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  pinMode(AZERO,INPUT);
  pinMode(RED_PIN,OUTPUT);
  pinMode(GREEN_PIN,OUTPUT);
  pinMode(BLUE_PIN,OUTPUT);
};

// the loop routine runs over and over again forever:
void loop() {

  
  if(Serial.available() > 0){

    String msg = Serial.readString();
    if(msg == "RV!"){

    int rawSensorValue = analogRead(AZERO);
    digitalWrite(GREEN_PIN,HIGH);

    //float amperage = voltage / resistance;

    // print out the value you read:
    Serial.print("AZEROVOLTAGE!");
    Serial.print(rawSensorValue);
    Serial.print("!QRT");
    delay(100);
    digitalWrite(GREEN_PIN,LOW);
    }
    else{
      digitalWrite(RED_PIN,HIGH);
      delay(100);
      digitalWrite(RED_PIN,LOW);

     


    };
    delay(1);

  };
}
