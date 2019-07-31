# Stadtreinigung Hamburg Custom Component

![Stadtreinigung Hamburg][srh]

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

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[exampleimg]: example.png
[srh]: https://upload.wikimedia.org/wikipedia/de/7/77/Stadtreinigung_Hamburg_logo.svg
