# Mirrorman
Mirrorman is a mirror management daemon for Ultramarine Linux mirrors.

# Installation

Simply clone this repository and run `pip install .`

# Usage

To configure Mirrorman, Add an environment variable called `MIRRORMAN_CONFIG` on runtime pointing to the configuration file. Examples are available in `mirrorman.cfg.example`.

Then run Mirrorman in the background or add it as a service.