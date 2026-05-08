#!/usr/bin/env sh
# initdocs install script
# Installs initdocs via uv (preferred) or downloads a standalone binary as fallback.
# Usage: curl -fsSL "https://raw.githubusercontent.com/martinjnilsen/initdocs/main/scripts/install.sh" | sh

set -eu

RELEASES_URL="https://github.com/martinjnilsen/initdocs/releases"
REPO_URL="https://github.com/martinjnilsen/initdocs"
INSTALL_DIR="$HOME/.local/bin"
BINARY_NAME="initdocs"
VERBOSE=false
DEBUG=false
DRY_RUN=false
RELEASE_TAG=""
STANDALONE=false

# ── Flags ─────────────────────────────────────────────────────────────────────

while [ $# -gt 0 ]; do
  case "$1" in
    --verbose)    VERBOSE=true ;;
    --debug)      DEBUG=true ;;
    --dry-run)    DRY_RUN=true ;;
    --standalone) STANDALONE=true ;;
    --release)
      [ $# -ge 2 ] || { printf "[error] --release requires a tag argument (e.g. --release v1.1.6)\n\n"; exit 1; }
      RELEASE_TAG="$2"
      shift
      ;;
    help)
      printf "Usage: sh install.sh [--verbose] [--debug] [--dry-run] [--standalone] [--release <tag>] [help]\n\n"
      printf "  --verbose          Print all steps and output during installation.\n"
      printf "  --debug            Print debug information for troubleshooting.\n"
      printf "  --dry-run          Preview what would happen without making any changes.\n"
      printf "  --standalone       Skip uv and use the standalone binary installer directly.\n"
      printf "  --release <tag>    Install a specific release (e.g. --release v1.1.6).\n"
      printf "                     Defaults to the latest release.\n"
      printf "  help               Show this help message.\n\n"
      printf "Run from anywhere or pipe directly:\n"
      printf "  curl -fsSL \"%s/main/scripts/install.sh\" | sh\n\n" "https://raw.githubusercontent.com/martinjnilsen/initdocs"
      exit 0
      ;;
    *)
      printf "[error] Unknown argument: %s\n\n" "$1"
      printf "Usage: sh install.sh [--verbose] [--debug] [--dry-run] [--release <tag>] [help]\n\n"
      exit 1
      ;;
  esac
  shift
done

# ── Helpers ───────────────────────────────────────────────────────────────────

cmd()     { $VERBOSE && printf "> %s\n" "$*" || true; }
info()    { $VERBOSE && printf "[info] %s\n" "$*" || true; }
warning() { printf "[warning] %s\n" "$*"; }
error()   { printf "[error] %s\n\n" "$*"; exit 1; }
item()    { $VERBOSE && printf "  - %s\n" "$*" || true; }
debug()   { $DEBUG && printf "[debug] %s\n" "$*" || true; }
dryrun()  { $DRY_RUN && printf "[dry-run] %s\n" "$*" || true; }

# run <description> <cmd...>
# In dry-run mode: prints what would run. Otherwise: executes the command.
run() {
  local desc="$1"; shift
  if $DRY_RUN; then
    printf "[dry-run] %s\n" "$desc"
  else
    "$@"
  fi
}

debug "Flags: VERBOSE=$VERBOSE DEBUG=$DEBUG DRY_RUN=$DRY_RUN STANDALONE=$STANDALONE RELEASE_TAG=${RELEASE_TAG:-<latest>}"

$DRY_RUN && printf "[dry-run] Previewing installation — no changes will be made.\n\n"

# ── uv detection ─────────────────────────────────────────────────────────────

if ! $STANDALONE && command -v uv >/dev/null 2>&1; then
  debug "uv found at: $(command -v uv)"

  if [ -n "$RELEASE_TAG" ]; then
    VERSION=$(printf "%s" "$RELEASE_TAG" | sed 's/^v//')
    PACKAGE="initdocs==$VERSION"
  else
    PACKAGE="initdocs"
  fi

  cmd "Installing $PACKAGE via uv tool install..."
  if $DRY_RUN; then
    dryrun "Would run: uv tool install $PACKAGE"
    printf "\n[dry-run] Preview complete. Run without --dry-run to install.\n"
  else
    uv tool install "$PACKAGE"
    printf "\n[info] initdocs installed via uv.\n"
    printf "[info] Run: initdocs --help\n\n"
  fi
  exit 0
fi

if ! $STANDALONE; then
  warning "uv not found. Falling back to standalone binary installer."
  printf "\n"
fi

# ── Preflight ─────────────────────────────────────────────────────────────────

debug "Checking for curl..."
command -v curl >/dev/null 2>&1 || error "curl is required but not found. Please install curl and try again."
debug "curl found at: $(command -v curl)"

# ── OS / architecture detection ───────────────────────────────────────────────

OS=$(uname -s)
ARCH=$(uname -m)
debug "Detected OS: $OS, ARCH: $ARCH"

case "$OS" in
  Linux)
    PLATFORM="linux"
    ;;
  Darwin)
    case "$ARCH" in
      arm64)
        PLATFORM="macos_arm"
        ;;
      x86_64)
        warning "No native Intel macOS binary is available."
        printf "\n"
        if $DRY_RUN; then
          dryrun "Would prompt: Try the Linux binary as a fallback? [y/N]"
          PLATFORM="linux"
        else
          printf "The Linux binary may work in compatible environments (e.g. via Rosetta 2).\n"
          printf "Try the Linux binary as a fallback? [y/N] "
          if read ANSWER </dev/tty 2>/dev/null; then
            case "$ANSWER" in
              [yY]|[yY][eE][sS])
                PLATFORM="linux"
                info "Proceeding with Linux binary."
                ;;
              *)
                printf "\nDownload the binary manually from:\n  %s\n\n" "$RELEASES_URL"
                exit 0
                ;;
            esac
          else
            printf "\nCannot read input interactively. Download the binary manually from:\n  %s\n\n" "$RELEASES_URL"
            exit 1
          fi
        fi
        ;;
      *)
        error "Unsupported architecture: $ARCH. Download manually from: $RELEASES_URL"
        ;;
    esac
    ;;
  MSYS*|MINGW*|CYGWIN*)
    error "Native Windows is not supported by this script.\nDownload the .exe from: $RELEASES_URL\nFor a shell-friendly setup, consider using WSL."
    ;;
  *)
    error "Unsupported OS: $OS. Download manually from: $RELEASES_URL"
    ;;
esac

debug "Platform: $PLATFORM"

# ── Resolve release tag ───────────────────────────────────────────────────────

if [ -n "$RELEASE_TAG" ]; then
  cmd "Using specified release: $RELEASE_TAG"
  TAG="$RELEASE_TAG"
  if $DRY_RUN; then
    dryrun "Would use specified tag: $TAG"
  else
    debug "Using specified tag: $TAG"
  fi
else
  cmd "Fetching latest release version..."
  if $DRY_RUN; then
    dryrun "Would fetch latest tag from: $REPO_URL/releases/latest"
    TAG="v?.?.?"
  else
    debug "Following GitHub redirect from $REPO_URL/releases/latest..."
    LATEST_URL=$(curl -Ls -o /dev/null -w "%{url_effective}" "$REPO_URL/releases/latest")
    TAG=$(printf "%s" "$LATEST_URL" | sed 's|.*/tag/||')
    debug "Redirect URL: $LATEST_URL"
    debug "Resolved tag: $TAG"
    info "Latest version: $TAG"
  fi
fi

# ── Construct download URL ────────────────────────────────────────────────────

FILENAME="${BINARY_NAME}_${TAG}_${PLATFORM}"
DOWNLOAD_URL="$REPO_URL/releases/download/$TAG/$FILENAME"
debug "Download URL: $DOWNLOAD_URL"

# ── Validate release exists ───────────────────────────────────────────────────

cmd "Validating release $TAG for $PLATFORM..."
if $DRY_RUN; then
  dryrun "Would validate release exists (HEAD $DOWNLOAD_URL)"
else
  debug "HEAD check: $DOWNLOAD_URL"
  if ! curl -fsLI "$DOWNLOAD_URL" -o /dev/null 2>/dev/null; then
    error "Release $TAG not found for platform $PLATFORM.\nCheck available releases at: $RELEASES_URL"
  fi
  debug "Release validated."
fi

# ── Create install directory ──────────────────────────────────────────────────

cmd "Preparing install directory: $INSTALL_DIR..."
run "Would create install directory: $INSTALL_DIR" mkdir -p "$INSTALL_DIR"

# ── Download binary ───────────────────────────────────────────────────────────

cmd "Downloading $BINARY_NAME $TAG for $PLATFORM..."
if $DRY_RUN; then
  dryrun "Would download $DOWNLOAD_URL → $INSTALL_DIR/$BINARY_NAME"
else
  TMP_FILE=$(mktemp)
  debug "Temp file: $TMP_FILE"
  debug "Downloading: $DOWNLOAD_URL"
  if ! curl -fsSL "$DOWNLOAD_URL" -o "$TMP_FILE"; then
    rm -f "$TMP_FILE"
    error "Download failed. Check your connection or visit:\n  $RELEASES_URL"
  fi
  mv "$TMP_FILE" "$INSTALL_DIR/$BINARY_NAME"
  debug "Binary installed to: $INSTALL_DIR/$BINARY_NAME"
fi

# ── Permissions + macOS quarantine ───────────────────────────────────────────

cmd "Setting permissions..."
if $DRY_RUN; then
  dryrun "Would chmod +x $INSTALL_DIR/$BINARY_NAME"
  if [ "$OS" = "Darwin" ]; then
    dryrun "Would clear macOS quarantine flag: xattr -d com.apple.quarantine $INSTALL_DIR/$BINARY_NAME"
  fi
else
  chmod +x "$INSTALL_DIR/$BINARY_NAME"
  debug "chmod +x applied."
  if [ "$OS" = "Darwin" ]; then
    xattr -d com.apple.quarantine "$INSTALL_DIR/$BINARY_NAME" 2>/dev/null || true
    debug "Quarantine flag cleared (or not present)."
  fi
fi

# ── Detect shell rc file ──────────────────────────────────────────────────────

SHELL_NAME=$(basename "$SHELL")
debug "Shell: $SHELL_NAME, OS: $OS"

case "$SHELL_NAME" in
  zsh)
    RC_FILE="$HOME/.zshrc"
    ;;
  bash)
    if [ "$OS" = "Darwin" ]; then
      RC_FILE="$HOME/.bash_profile"
    else
      RC_FILE="$HOME/.bashrc"
    fi
    ;;
  *)
    RC_FILE="$HOME/.profile"
    ;;
esac

debug "RC file: $RC_FILE"

# ── Add ~/.local/bin to PATH ──────────────────────────────────────────────────

PATH_LINE='export PATH="$HOME/.local/bin:$PATH"'
SEARCH_PATTERN=".local/bin"

cmd "Checking PATH in $RC_FILE..."
if $DRY_RUN; then
  dryrun "Would check if $SEARCH_PATTERN is already in $RC_FILE"
  dryrun "Would append to $RC_FILE (if not present): $PATH_LINE"
else
  if [ -f "$RC_FILE" ] && grep -q "$SEARCH_PATTERN" "$RC_FILE"; then
    info "$INSTALL_DIR already on PATH in $RC_FILE — skipping."
  else
    printf '\n# Added by initdocs installer\n%s\n' "$PATH_LINE" >> "$RC_FILE"
    info "Added $INSTALL_DIR to PATH in $RC_FILE."
  fi
fi

# ── Done ──────────────────────────────────────────────────────────────────────

if $DRY_RUN; then
  printf "\n[dry-run] Preview complete. Run without --dry-run to install.\n"
else
  printf "\n[info] initdocs %s installed to %s/%s\n" "$TAG" "$INSTALL_DIR" "$BINARY_NAME"
  printf "[info] To apply the PATH update, run:\n\n"
  printf "  source %s\n\n" "$RC_FILE"
  printf "Or open a new terminal, then run: initdocs --help\n\n"
fi
