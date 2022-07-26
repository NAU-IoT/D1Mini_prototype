/*
 * constants that will be used through this program
 */
// define WiFi credentials
#define ssid "slurricane"
#define WPA2 "PASSWORD"

// MQTT credentials
#define mqtt_server "192.169.1.10"      // MQTT broker IP (RPI 4 in this instance)
#define mqtt_user "akiel"
#define mqtt_pass "password"
#define clientID "client_area"

// MQTT topics
#define temp_topic "home/area/BME_temp"
#define hum_topic "home/area/BME_hum"
#define press_topic "home/area/BME_press"
#define alt_topic "home/area/BME_alt"

// BME280  
#define SEALEVELPRESSURE_HPA (1013.25)

// hex addresses
#define SHT_ADDR (0X44)
#define BME_ADDR (0x77)
#define LCD_ADDR (0x27)

// pins for LED visual error checking
//#define LED_RED 8
//#define LED_YELLOW 9
