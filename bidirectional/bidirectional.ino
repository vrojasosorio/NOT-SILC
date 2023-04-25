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

#define HOLD_BALL  1
#define LOAD_BALL  2
#define DROP_BALL  3
#define SET_DISTANCE 4
#define MANUAL_HOME 5
#define RESET_HOME 6
#define NOT_HOLD 7


#define PRINT 25
#define LOADED 10
#define HELD 11
#define DROPPED 12
#define DISTANCE_SETTED 13
#define HOME_READY 23
#define HOME_RESETTED 14


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
        
      case LOAD_BALL:
        blinkLed(1000);
        delay(2000);

        packet.bytes[0] = LOADED;
        packet.bytes[1] = 6;
        
        for (int i = 0; i < numBytes; i++) {
          Serial.write(packet.bytes[i]);
        }
        Serial.flush();
        break;
      
      case HOLD_BALL:
      
        delay(1000);

        packet.bytes[0] = HELD;
        packet.bytes[1] = 6;
        
        for (int i = 0; i < numBytes; i++) {
          Serial.write(packet.bytes[i]);
        }
        Serial.flush();
        break;

      case DROP_BALL:
        blinkLed(1000);
        delay(1000);

        packet.bytes[0] = DROPPED;
        packet.bytes[1] = 6;
        
        for (int i = 0; i < numBytes; i++) {
          Serial.write(packet.bytes[i]);
        }
        
        Serial.flush();
        break;

      case SET_DISTANCE:
        if (packet.unpacked.data > 150) {
          digitalWrite(13, HIGH);
          delay(5000);
          digitalWrite(13,LOW);
          
        } else {
          blinkLed(500);
        }

        packet.bytes[0] = DISTANCE_SETTED;
        packet.bytes[1] = 6;
        
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
