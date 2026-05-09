#include<WiFi.h>

                                             String currentMode = "SCAN";

// 🔹 Convert encryption type to readable text
String getEncryptionType(wifi_auth_mode_t encryptionType)
{
    switch (encryptionType)
    {
    case WIFI_AUTH_OPEN:
        return "OPEN";
    case WIFI_AUTH_WEP:
        return "WEP";
    case WIFI_AUTH_WPA_PSK:
        return "WPA";
    case WIFI_AUTH_WPA2_PSK:
        return "WPA2";
    case WIFI_AUTH_WPA_WPA2_PSK:
        return "WPA/WPA2";
    case WIFI_AUTH_WPA2_ENTERPRISE:
        return "WPA2-ENT";
    case WIFI_AUTH_WPA3_PSK:
        return "WPA3";
    default:
        return "UNKNOWN";
    }
}

// 🔥 Switch to SCAN mode
void startScanMode()
{
    WiFi.softAPdisconnect(true); // clean AP
    delay(500);

    WiFi.mode(WIFI_STA);
    WiFi.disconnect(true);

    currentMode = "SCAN";
    Serial.println("MODE:SCAN");
}

// 🔥 Switch to SIMULATION mode
void startSimulationMode()
{
    WiFi.disconnect(true);
    delay(500);

    WiFi.mode(WIFI_AP);

    // Fake open WiFi
    WiFi.softAP("Free_Public_WiFi");

    currentMode = "SIMULATION";
    Serial.println("MODE:SIMULATION");
}

// 🔹 Read commands from Serial (START_SIM / STOP_SIM)
void checkSerialCommand()
{
    if (Serial.available())
    {
        String cmd = Serial.readStringUntil('\n');
        cmd.trim();

        if (cmd == "START_SIM")
        {
            startSimulationMode();
        }
        else if (cmd == "STOP_SIM")
        {
            startScanMode();
        }
    }
}

void setup()
{
    Serial.begin(115200);
    delay(1000);

    startScanMode(); // default mode
}

// 🔥 SCAN MODE
void scanNetworks()
{
    Serial.println("SCAN_START");

    int n = WiFi.scanNetworks();

    if (n > 0)
    {
        for (int i = 0; i < n; i++)
        {

            String ssid = WiFi.SSID(i);
            String bssid = WiFi.BSSIDstr(i);
            int rssi = WiFi.RSSI(i);
            int channel = WiFi.channel(i);
            String encryption = getEncryptionType(WiFi.encryptionType(i));

            // JSON output
            String json = "{";
            json += "\"ssid\":\"" + ssid + "\",";
            json += "\"bssid\":\"" + bssid + "\",";
            json += "\"encryption\":\"" + encryption + "\",";
            json += "\"rssi\":" + String(rssi) + ",";
            json += "\"channel\":" + String(channel);
            json += "}";

            Serial.println(json);
        }
    }

    Serial.println("SCAN_END");
}

// 🔥 SIMULATION MODE
void simulationMode()
{
    // Simulated device logs (for demo)
    String devices[] = {
        "FA:89:02:AA:B4:7B",
        "F2:60:B8:00:C6:FC"};

    for (int i = 0; i < 2; i++)
    {
        String json = "{";
        json += "\"device_id\":\"" + devices[i] + "\",";
        json += "\"action\":\"connected\"";
        json += "}";

        Serial.println(json);
        delay(2000);
    }
}

void loop()
{
    checkSerialCommand();

    if (currentMode == "SCAN")
    {
        scanNetworks();
        delay(8000);
    }
    else if (currentMode == "SIMULATION")
    {
        simulationMode();
    }
}