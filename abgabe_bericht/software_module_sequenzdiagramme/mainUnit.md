
```mermaid
sequenceDiagram
    participant ada_fruit
    participant raspberry_pi
    participant data_base
    ada_fruit->>raspberry_pi: sends data via bluetooth
    raspberry_pi->>ada_fruit: return status connection
    raspberry_pi->>data_base: sends data via http
```
