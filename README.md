# How to run
## Locally

Use
```bash
python -m src.main
```
directly inside the parent folder to the src-folder to run the program locally.

## Install
We use [PyInstaller](https://pyinstaller.org/en/stable/) to create an executable file.
Following are the settings.
Its also recommended that [Auto-Py-To-Exe](https://pypi.org/project/auto-py-to-exe/) is used as it's a gui for PyInstaller

|Name|Value|
|-|-|
|Console-Window|Window based|
|Additional-files|The `src/` folder must be specified as `src/` here|
|Advanced >> `--path`|Specify the parent foler of `src`, so `src/../` here|
|Script location|`src/main.py`|