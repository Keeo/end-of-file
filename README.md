# End of file
End of file is formatter to ensure text files always end with one newline. Eof is able to resolve every possible situation - missing newline, more then one newline and whitespaces mixed with newlines. Eof is heavily configurable using parameters, no config file is needed.

Configurable options:
 - include or exclude hidden files (file or folders starting with dot)
 - blacklisted strings that are found inside traversed paths
 - whitelisted extensions
 - identification of text files (mimetype or bruteforce)
 - validation only mode for ci pipelines

The code is short and dead simple so if you have more questions feel free to open an issue or take a look into [src](https://github.com/Keeo/end-of-file/blob/master/src/end_of_file/__init__.py).

## Installation

End_of_file is python script and thus python3.6 or newer must be present on the system. Eof is just another pip package and can be installed with `pip install end-of-file`.

## Usage

Installation adds Eof to your environment so feel free to try
```sh
eof --help
```

To format project
```sh
eof --path=./project
```

To format only specific extensions
```sh
eof --path=./project --extensions=txt,md,py,rb,cpp
```

To check in ci/cd if project is formatted correctly, return 0 if yes, 1 if changes are needed. Files are not changed.
```sh
eof --path=./project --check
```

In case you have for example build destination in your project and want to skip it you can use --ignore flag. Paths with substring from this option are skipped.
```
eof --ignore /dist -i egg-info
```

Circleci job example
```yaml
circleci-job:
  docker:
    - image: circleci/python:3
  steps:
    - checkout
    - run: pip install end-of-file
    - run: eof --check
```

## Strategies
Eof needs to have a way to identify files that should be checked for correct newline. There are two options to choose from.

### Bruteforce (default)
Bruteforce strategy just opens the file and tries to read first line, if that does not work it assumes the file does not contain text and is skipped. This should be the most precise but may take more time.

```sh
eof --strategy='bruteforce'
```

### Mimetype
Mimetype strategy checks extensions against lookup table.

```sh
eof --strategy='mimetype'
```

## Testing
Code is fairly well tested, feel free to take a [look](https://github.com/Keeo/end-of-file/tree/master/tests).

## License
BSD 3-Clause
