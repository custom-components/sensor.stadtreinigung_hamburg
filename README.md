![Stadtreinigung Hamburg][srh]

<h2 align="center">Stadtreinigung Hamburg Custom Component</h2>

<p align="center">
  <a href="https://github.com/custom-components/hacs"><img alt="Code style: black" src="https://img.shields.io/badge/HACS-Default-orange.svg"></a>
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
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
          {% set collection = states.sensor.stadtreinigung_hamburg_sesamstrasse_blaue_papiertonne.state %}
          {% set tomorrow = (as_timestamp(now()) + 86400)|timestamp_custom("%Y-%m-%d") %}
          {{ collection == tomorrow }}
```

Do you have some other examples? Make a PR and add it here.

## Contributions are welcome!

If you want to contribute to this, please read the [Contribution guidelines](CONTRIBUTING.md)


[exampleimg]: example.png
[srh]: https://upload.wikimedia.org/wikipedia/de/7/77/Stadtreinigung_Hamburg_logo.svg
