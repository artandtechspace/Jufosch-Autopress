
This is a simple reference file, no full README

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


### Windows
MineGw (MSys2) installieren und darüber dann python, pip und über pacman dann die speziellen Python-packete

packages.msys2.org/package/mingw-w64-x86_64-python-[PACKAGE] zb. pillow oder lxml

# I18n

Most of the below bases on [this](https://simpleit.rocks/python/how-to-translate-a-python-project-with-gettext-the-easy-way/)

## Getting all messages
To extract all getText-Messages, run
```bash
find src/ -name "*.py" -o -name "*.glade" | xargs xgettext -d jufusch-presentation-tool -o locale/jufusch-presentation-tool.pod
```

## Creating a new language

inside the parent folder of src/

Using
```bash
msginit -i locale/jufusch-presentation-tool.pod --locale=de_DE -o locale/de/LC_MESSAGES/jufusch-presentation-tool.po
```

you can create a new translation as in the example for the german language.

It will be based on the previously gathered messages `locale/jufusch-presentation-tool.pod` file.

To continue go to the section `Finalising a language`

## Updating a language

After you re-gathered all messages using the cmd given above, run

```bash
msgmerge --update locale/de/LC_MESSAGES/jufusch-presentation-tool.po locale/jufusch-presentation-tool.pod
```

to merge them with the already existing translations.

Be sure to search for all contradicting elements using the `fuzzy` keyword inside the merged file and also add all missing translations

To continue go to the section `Finalising a language`

## Finalising a language

Using

```bash
msgfmt -o locale/de/LC_MESSAGES/jufusch-presentation-tool.mo locale/de/LC_MESSAGES/jufusch-presentation-tool.po
```

*Using german language as an example here*

you generate the binary language file that will be used by the program