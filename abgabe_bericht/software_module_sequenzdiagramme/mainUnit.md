
```mermaid
sequenceDiagram
    participant adafruit
    participant raspberry_pi
    participant data_base
    adafruit->>raspberry_pi: sends data via bluetooth
    raspberry_pi->>adafruit: return status connection
    raspberry_pi->>data_base: sends data via http
```
