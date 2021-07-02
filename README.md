# End of file
End of file is formatter for dealing with new lines at the end of the files. Eof can remove extra new lines and white spaces, or add missing one if needed. It accepts lists of extensions to look for but can also use own strategy to find text files, hidden files and folders are ignored. It needs python to run but because it's only purpose is to ensure file ends with exactly one new line at the end it can be used to format any type of programming languages or text files.

The code is short and dead simple so if you have more questions feel free to open an issue or take a look into [src](https://github.com/Keeo/end-of-file/blob/master/src/end_of_file/__init__.py).


## Installation and usage

### Installation

End_of_file is python script and thus python3.6 or newer must be present on the system. Eof is just another pip package and can be installed with `pip install end-of-file`.

### Usage

Installation adds Eof to your environment so feel free to try
```sh
eof --help
```

To format project
```sh
eof --path=./project
```

To format only specific extensions (case insensitive)
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

#### Strategies
In case extensions flag is not provided eof has two ways of determining if file should be considered.

#### Bruteforce (default)
Bruteforce strategy just opens the file and tries to read first line, if that does not work it assumes the file does not contain text and is skipped.

```sh
eof --strategy='bruteforce'
```

#### Mimetype
Mimetype strategy checks extensions against lookup table.

```sh
eof --strategy='mimetype'
```

## Testing
Code is fairly well tested, feel free to take a [look](https://github.com/Keeo/end-of-file/tree/master/tests).

## License
BSD 3-Clause
