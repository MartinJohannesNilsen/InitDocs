
# InitDocs

<img src="https://i.ibb.co/S3mbGrB/Init-Docs-HD-720p-3.gif" width="600"/>

Welcome to InitDocs - a command line tool for initializing and managing documentation projects based on [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Usage

```
> initdocs --help
usage: initdocs [-h] [-p PATH] [-d DIR_NAME] [--print-config | --no-print-config]

Command Line Interface to create and update mkdocs documentation projects.

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  documentation directory, prompted if not set
  -d DIR_NAME, --dir-name DIR_NAME
                        name of the directory, if not default "docs"
  --print-config, --no-print-config
                        print the content of "mkdocs.yml" and exit
```

> Here, we have added an alias inside our .zshrc file, with the absolute path to the executable. This enables us to run it from any working directory in the terminal.

## Installation

To be able to use the command line tool, we would need to get access to the executable program. As of now, we build executables for MacOS (arm), Windows and Linux (Ubuntu). If none of these works for you, you may build the executable yourself - which will be described further down.

## Using Released Executable

After having downloaded the correct executable, and placed it in a location of your choice, we should make it available in your terminal.

The very first step you will have to take is to make it executable. This might not be necessary, but in most cases it would. This can be done by appending the execute permission to the file as such:

```bash
chmod +x initdocs
```

> On MacOS, you will probably also need to allow the use of it in the privacy and security settings. This will be prompted when run for the first time.

Then, we would like to ensure that your terminal recognizes the application, regardless of working directory. For this, the simplest approach is to create an alias to the executable in your shell configuration file (UNIX systems). For Windows users, you can append the path to the executable in your environment variables, or just [start using WSL already](https://blog.mjntech.dev/posts/oLQQE3ruoZyCaASbwtqK#First_Step:_Make_Sure_You_Have_Zsh_Installed_and_Set_as_Default_Shell).

First, we need to grab the path to the directory of the executable. This name or path does not matter, but we rename the executable to `initdocs[.exe]` out of preference. For getting the path, you can utilize the `pwd` command in your terminal to print the absolute path of your current working directory.

Then, in you shell configuration file (e.g. .zshrc or .bashrc), you would like to add an alias in the format of 

```
export initdocs=<abs_path_to_executable>
```
where initdocs will be the command name. After saving the file, you can open a new terminal, or reset the current one by sourcing the configuration file: 

```bash
# Source UNIX shell config
source .[bash/zsh][rc/_profile]
```


## Build Executable

For simplicity, we provide a makefile with predefined commands for setting up a Python virtual environment, installing dependencies and building a wheel or executable. 

To build an executable for your system, simply use the following command:

```bash
make executable
```

<details>
<summary>No access to make on your operating system?</summary>

<br/>

You can run the commands directly instead. If you are using virtual environments, the only part that is not OS-agnostic is the activation of the venv.

**Step 1a. Setup Venv in UNIX (macos/linux/wsl)**
```bash
# Create virtual environment
python -m venv .venv

# Activate venv
source .venv/bin/activate
```

**Step 1b. Setup Venv in Windows Powershell**
```bash
# Create virtual environment
python -m venv .venv

# Activate venv
.\.venv\Scripts\activate.ps1
```

**Step 1b. Setup Venv in Windows CMD**
```bash
# Create virtual environment
python -m venv .venv

# Activate venv
.\.venv\Scripts\activate
```

**Step 2. Make Executable**
```bash
# Install dependencies
pip install --upgrade pip setuptools wheel
pip install --require-virtualenv ".[build]"

# Build wheel
python -m build

# Build executable
pyinstaller initdocs.spec
```

</details>
<br/>

The executable will be created in the `dist` directory. Now you may follow the steps described in the prior subsection for adding an alias to you shell configuration file.

## Further Development

> We highly recommend developing in a UNIX environment. For Windows users, this yields a fantastic opportunity to get familiar with WSL. If you want some help getting started, I have written a post on the subject, available [here](https://blog.mjntech.dev/posts/oLQQE3ruoZyCaASbwtqK#First_Step:_Make_Sure_You_Have_Zsh_Installed_and_Set_as_Default_Shell).

### Configure Virtual Environment With Dependencies

Using the makefile, we can setup a virtual environment and install the dependencies. For installing the dependencies to run the script, use `make install-deps`. If you want to be able to build the project (as wheel/executable), use `make install-build-deps`. 

```bash
# Alternative 1: Setup venv and install required dependencies
make install-deps

# Alternative 2: Setup venv, install required dependencies and build dependencies
make install-build-deps
```

### Source Virtual Environment

The virtual environment can be activated by running the following command based on your system:

```bash
# Unix / WSL
source .venv/bin/activate

# Windows
# .\.venv\Scripts\activate # CMD
# .\.venv\Scripts\activate.ps1 # Powershell
```

You should now be ready for further development!

### Test Your Changes

To test your changes before building the executable, ensure that the script runs without failure (remember to activate/source the virtual environment) using the following command:

```
python src/initdocs
```

## Alter the template

To effectively modify the template, it's helpful to view the changes in real time. This can be achieved by serving the template through the dedicated Docker Compose service. The only step needed is to uncomment the `site_name` in the `src/template/mkdocs.yml`, as this must be defined.

```bash
# Navigate to template dir
cd src/template

# Define sitename
sed -i "s/# site_name: \"\"/site_name: \"Template\"/" mkdocs.yml

# Run docker compose service: docs-serve
docker compose up docs-serve -d
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/MartinJohannesNilsen/InitDocs/?tab=License-1-ov-file)
