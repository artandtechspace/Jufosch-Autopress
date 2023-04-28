# What is this Project?

This is a small internal program to fill a power-point-presentation (PPP) with jufo-data (Mainly members and project) and also to directly assign prices to them.

It's based on the [PyGObject](https://www.gtk.org/docs/language-bindings/python/) (Gtk + Python) and uses [python-pptx](https://python-pptx.readthedocs.io/en/latest/index.html) to read/write presentations.


# How to run

**Check the windows-section below as it's a bit trick to run there**

Firstly you need to have installed the required librarys

|Software|Info|
|-|-|
|[PyGObject](https://www.gtk.org/docs/language-bindings/python/)||
|[python-pptx](https://python-pptx.readthedocs.io/en/latest/index.html)||
|[gettext](https://www.gnu.org/software/gettext/) (Often already preinstalled)|Linux only, the windows version currently doesn't support multiple languages|

## For windows
All of the instructions below wont work out of the box, you need to install [MinWG](https://sourceforge.net/projects/mingw/).
Then install all required python-librarys through their CLI (MSys2). For that you need to use pacman.

To install a specific python package, go to
[packages.msys2.org/package/mingw-w64-x86_64-python-{PACKAGE}](
packages.msys2.org/package/mingw-w64-x86_64-python-{PACKAGE}) where you replace `{PACKAGE}` with for example `pillow` or `lxml`.

## Running locally

Use
```bash
python -m src.main
```
directly inside the parent folder to the `src`-folder to run the program locally.

## Install
We use [PyInstaller](https://pyinstaller.org/en/stable/) to create an executable file.
Following are the settings.
Its also recommended that [Auto-Py-To-Exe](https://pypi.org/project/auto-py-to-exe/) is used as it's a gui for PyInstaller **(Work on linux as well as on windows)**

|Name|Value|
|-|-|
|Console-Window|Window based|
|Additional-files|The `src/` folder must be specified as `src/` here|
|Advanced >> `--path`|Specify the parent foler of `src`, so `src/../` here|
|Script location|`src/main.py`|
|Advanced >> `--name`|`Jufusch-Autopress`|

# I18n

Most of the instructions below are based on [this](https://simpleit.rocks/python/how-to-translate-a-python-project-with-gettext-the-easy-way/).

## Getting all messages
To extract all getText-Messages, run
```bash
find src/ -name "*.py" -o -name "*.glade" | xargs xgettext -d jufusch-presentation-tool -o locale/jufusch-presentation-tool.pod
```

## Creating a new language

inside the parent folder of `src/`

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

you generate the binary language file that will be used by the program.