
```mermaid
sequenceDiagram
    participant adafruit_ppm_c_%
    participant adafruit_window
    participant adafruit_people
    participant raspberry_pi
    participant data_base
    raspberry_pi->>adafruit_ppm_c_%: try to connect
    adafruit_ppm_c_%->>raspberry_pi: return connection established
    raspberry_pi->>data_base: sends data via http
```
