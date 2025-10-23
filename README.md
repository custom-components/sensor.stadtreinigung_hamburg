![Stadtreinigung Hamburg][srh]

<h2 align="center">Stadtreinigung Hamburg Custom Component</h2>

<p align="center">
  <a href="https://github.com/hacs/integration"><img alt="Code style: black" src="https://img.shields.io/badge/HACS-Default-orange.svg"></a>
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
  <a href=""><img alt="Hamburg" src="https://img.shields.io/badge/city-hamburg-e3000f"></a>
  <a href="https://github.com/custom-components/sensor.stadtreinigung_hamburg/issues"><img alt="Open Issues" src="https://img.shields.io/github/issues/custom-components/sensor.stadtreinigung_hamburg"></a>
  <a href="https://github.com/custom-components/sensor.stadtreinigung_hamburg/releases"><img alt="Release" src="https://img.shields.io/github/release/custom-components/sensor.stadtreinigung_hamburg"></a>
</p>

<p><br /></p>

**This component will set up the following sensors**

- schwarze Restmülltonne
- blaue Papiertonne
- gelbe Wertstofftonne/-sack
- grüne Biotonne
- Weihnachtsbäume
- Laubsäcke

The state of these sensors will be the next collection date.

![example][exampleimg]

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `stadtreinigung_hamburg`.
4. Download _all_ the files from the `custom_components/stadtreinigung_hamburg/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Stadtreinigung Hamburg"

## Examples

Below are some use cases for this sensor

### Binary Sensor: Garbage Collection Tomorrow
The `binary_sensor` will be on if the collection is tomorrow:

```yaml
binary_sensor:
  - platform: template
    sensors:
      srh_morgen_sesamstrasse_blau:
        friendly_name: "blaue Papiertonne (morgen)"
        value_template: >-
          {% set collection = as_timestamp(states.sensor.stadtreinigung_hamburg_sesamstrasse_blaue_papiertonne.state)|timestamp_custom("%Y-%m-%d") %}
          {% set tomorrow = (as_timestamp(now()) + 86400)|timestamp_custom("%Y-%m-%d") %}
          {{ collection == tomorrow }}
```

Do you have some other examples? Make a PR and add it here.

### Sensor: Next Emptying Date

This example adds a `sensor` that displays the next emptying date. Below is a card wich uses this `sensor`. 
In addition, <a href="https://github.com/piitaya/lovelace-mushroom/releases">https://github.com/piitaya/lovelace-mushroom/releases</a> is also required for this example.

in configuration.yaml
```yaml
sensor:
  - platform: template
    sensors:
      naechster_muelltermin:
        friendly_name: "Nächster Mülltermin"
        value_template: >
          {% set sensors = {
            'Restmüll': 'sensor.stadtreinigung_hamburg_mull_schwarze_restmulltonne',
            'Papier': 'sensor.stadtreinigung_hamburg_mull_blaue_papiertonne',
            'Gelber Sack': 'sensor.stadtreinigung_hamburg_mull_gelbe_wertstofftonne_sack',
            'Biotonne': 'sensor.stadtreinigung_hamburg_mull_grune_biotonne'
          } %}
           {% set termine = namespace(liste=[]) %}
          {% for typ, entity in sensors.items() %}
            {% set wert = states(entity) %}
            {% if wert not in ['unknown', 'unavailable', '', None] %}
              {% set ts = as_timestamp(wert) %}
              {% set termine.liste = termine.liste + [ {'typ': typ, 'ts': ts} ] %}
            {% endif %}
          {% endfor %}
          {% if termine.liste | length > 0 %}
            {% set wochentage = {
                'Monday': 'Montag',
                'Tuesday': 'Dienstag',
                'Wednesday': 'Mittwoch',
                'Thursday': 'Donnerstag',
                'Friday': 'Freitag',
                'Saturday': 'Samstag',
                'Sunday': 'Sonntag'
            } %}
            {% set next = termine.liste | sort(attribute='ts') | first %}
            {% set day_en = as_datetime(next.ts).strftime('%A') %}
            {{ next.typ }} am {{ wochentage[day_en] }}, {{ as_datetime(next.ts).strftime('%d.%m.%Y') }}
          {% else %}
            Kein Termin gefunden
          {% endif %}
```
mushroom-template-card:

```yaml
type: custom:mushroom-template-card
entity: sensor.naechster_muelltermin
primary: |
  {{ states('sensor.naechster_muelltermin').split(' am ')[0] }}
secondary: |
  Abholung am {{ states('sensor.naechster_muelltermin').split(' am ')[1] }}
icon: >
  {% set typ = states('sensor.naechster_muelltermin').split(' am ')[0] | lower |
  replace('ü', 'ue') %} {% if 'restmuell' in typ %}
    mdi:trash-can
  {% elif 'papier' in typ %}
    mdi:recycle
  {% elif 'gelbersack' in typ %}
    mdi:sack
  {% elif 'biotonne' in typ %}
    mdi:leaf
  {% else %}
    mdi:trash-can-outline
  {% endif %}
icon_color: >
  {% set typ = states('sensor.naechster_muelltermin').split(' am ')[0] | lower |
  replace('ü', 'ue') %} {% if 'restmuell' in typ %}
    grey
  {% elif 'papier' in typ %}
    blue
  {% elif 'gelbersack' in typ %}
    yellow
  {% elif 'biotonne' in typ %}
    green
  {% else %}
    red
  {% endif %}
tap_action:
  action: more-info
grid_options:
  columns: 9
  rows: 1
```

## Contributions are welcome!

If you want to contribute to this, please read the [Contribution guidelines](CONTRIBUTING.md)


[exampleimg]: example.png
[srh]: https://upload.wikimedia.org/wikipedia/de/7/77/Stadtreinigung_Hamburg_logo.svg
