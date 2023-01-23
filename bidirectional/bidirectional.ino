/*
   by Gonzalo Olave
   license CC zero universal

   receive data structure from serial bus and blinks with function blinkLed()
   the echoes the bytes received

   modify for your own purposes

*/

// define data structure
// check data types here https://learn.sparkfun.com/tutorials/data-types-in-arduino/defining-data-types
#define numBytes 3
union {
  char bytes[numBytes];
  struct {
    // int in arduino are 2 bytes long
    uint8_t cmd; // B
    uint16_t data; // H
  } unpacked;
} packet;

#define TAKE_BALL 0
#define HOLD_BALL 1
#define DROP_BALL 2

#define TAKEN 3
#define SAVE_EXPERIMENT 4
#define SAVE_DATA 5
#define TAKEN 6

bool readPacket() {
  if (Serial.available() == numBytes) {
    // do nothing and wait if serial buffer doesn't have enough bytes to read
    Serial.readBytes(packet.bytes, numBytes);
    // read numBytes bytes from serial buffer and store them at a
    // union called “p  acket”
    return true;
  }
  else return false;
}

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(2000);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (readPacket() == true) {
    switch (packet.unpacked.cmd) {
      case DROP_BALL:
        blinkLed(100);
        break;
        
      case TAKE_BALL:
        blinkLed(1000);
        delay(2000);

        packet.bytes[0] = TAKEN;
        packet.bytes[1] = 6;
        
        for (int i = 0; i < numBytes; i++) {
          Serial.write(packet.bytes[i]);
        }
        Serial.flush();
        break;
        
      case SAVE_EXPERIMENT:
        blinkLed(500);
        delay(2000);

        packet.bytes[0] = SAVE_DATA;
        packet.bytes[1] = 9;

        for (int i = 0; i < numBytes; i++) {
          Serial.write(packet.bytes[i]);
        }
        Serial.flush();
        break;
    }
  }
}

void blinkLed(int t) {
  digitalWrite(13, HIGH);
  delay(t / 2);
  digitalWrite(13, LOW);
  delay(t / 2);
  digitalWrite(13, HIGH);
  delay(t / 2);
  digitalWrite(13, LOW);
  delay(t / 2);
}
