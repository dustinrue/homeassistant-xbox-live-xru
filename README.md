1. Create a custom_components/sensor directory structure in your configuration directory
1. Copy xru.py to the new sensor directory
1. Edit configuration.yml, add:
```
  sensor:
    - platform: xru
      gamertags:
        - gamertag1
        - gamertag2
```
