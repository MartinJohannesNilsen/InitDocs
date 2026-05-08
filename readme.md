
# initdocs

<img src="https://i.ibb.co/S3mbGrB/Init-Docs-HD-720p-3.gif" width="600"/>

Welcome to initdocs - a command line tool for initializing and managing documentation projects based on [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

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

### UNIX (Linux and macOS)

The script detects your OS, downloads the latest release to `~/.local/bin`, and adds it to your PATH:

```sh
curl -fsSL "https://raw.githubusercontent.com/martinjnilsen/initdocs/main/scripts/install.sh" | sh
```

Supports Linux and macOS (arm).

> **macOS Intel:** No native binary is available. The script will prompt you to try the Linux binary as a fallback.

<details>
<summary>More options — specific version, dry run, and manual inspection</summary>

**Install a specific version:**

```sh
curl -fsSL "https://raw.githubusercontent.com/martinjnilsen/initdocs/main/scripts/install.sh" | sh -s -- --release v1.1.6
```

**Preview what the script will do without making any changes:**

```sh
curl -fsSL "https://raw.githubusercontent.com/martinjnilsen/initdocs/main/scripts/install.sh" | sh -s -- --dry-run
```

**Download and inspect the script before running it:**

```sh
curl -fsSL "https://raw.githubusercontent.com/martinjnilsen/initdocs/main/scripts/install.sh" -o install.sh
# Review install.sh, then run with any flags:
sh install.sh                        # normal install (latest)
sh install.sh --release v1.1.6       # install a specific version
sh install.sh --dry-run              # preview only
sh install.sh --verbose              # print every step
sh install.sh --debug                # print debug output
sh install.sh help                   # show help
```

> **What does `sh -s -- <args>` mean?**
>
> - `-s` tells sh to read the script from stdin (the pipe) rather than a file.
> - `--` marks the end of sh's own options — everything after it is passed as arguments to the script itself.
> - Without `--`, a flag like `--dry-run` could be misinterpreted as a sh option rather than a script argument.

</details>

### Windows

Use the PowerShell installer:

```powershell
irm "https://raw.githubusercontent.com/martinjnilsen/initdocs/main/scripts/install.ps1" | iex
```

> **WSL or Git Bash?** Use the UNIX `curl` command above instead — it will install the Linux binary.

<details>
<summary>More options — specific version, dry run, and manual inspection</summary>

**Install a specific version:**

```powershell
& ([scriptblock]::Create((irm "https://raw.githubusercontent.com/martinjnilsen/initdocs/main/scripts/install.ps1"))) -Release v1.1.6
```

**Preview what the script will do without making any changes:**

```powershell
& ([scriptblock]::Create((irm "https://raw.githubusercontent.com/martinjnilsen/initdocs/main/scripts/install.ps1"))) -DryRun
```

**Download and inspect the script before running it:**

```powershell
Invoke-WebRequest "https://raw.githubusercontent.com/martinjnilsen/initdocs/main/scripts/install.ps1" -OutFile install.ps1
# Review install.ps1, then run with any flags:
.\install.ps1                        # normal install (latest)
.\install.ps1 -Release v1.1.6        # install a specific version
.\install.ps1 -DryRun                # preview only
.\install.ps1 -Verbose               # print every step
```

> **Note:** Running a downloaded `.ps1` requires execution policy to allow local scripts:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
> The `irm | iex` method above does not require this.

</details>


## Further Development

> We highly recommend developing in a UNIX environment. For Windows users, this yields a fantastic opportunity to get familiar with WSL. If you want some help getting started, I have written a post on the subject, available [here](https://blog.mjnlab.com/posts/terminal-essentials-a-step-by-step-setup-and-usage-tutorial#First_Step:_Make_Sure_You_Have_Zsh_Installed_and_Set_as_Default_Shell).

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

### Build Executable

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

**Step 1c. Setup Venv in Windows CMD**

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

The executable will be created in the `dist` directory. Move it to `~/.local/bin/` (or any directory on your `PATH`), then run `initdocs --help` to verify.

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
