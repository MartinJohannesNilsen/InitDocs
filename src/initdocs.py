from argparse import ArgumentParser, BooleanOptionalAction
from collections import defaultdict
from dataclasses import dataclass
from os import getcwd, remove
from os.path import abspath as os_path_abspath
from os.path import exists as os_path_exists
from pathlib import Path
from re import Pattern, compile, match, search, findall, escape, MULTILINE, DOTALL
from shutil import copytree, copy, rmtree
from sys import exit
from typing import Dict, List
from questionary import path as questionary_path
from questionary import select as questionary_select
from questionary import checkbox as questionary_checkbox
from questionary import text as questionary_text
from questionary import confirm as questionary_confirm
from questionary import Style as questionary_style
from questionary import Choice as questionary_choice
from ruamel.yaml import YAML
from ruamel.yaml.scanner import ScannerError
from ruamel.yaml.parser import ParserError


# Style

custom_style = questionary_style([
    ('qmark', 'fg:#673ab7 bold'),        # token in front of the question
    ('question', 'bold'),                # question text
    ('answer', 'fg:#f44336 bold'),       # submitted answer text behind the question
    ('pointer', 'fg:#f44336 bold'),      # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#f44336'),       # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#cc5454'),          # style for a selected item of a checkbox
    ('separator', 'fg:#cc5454'),         # separator in lists
    ('instruction', ''),                 # user instructions for select, rawselect, checkbox
    ('text', ''),                        # plain text
    ('disabled', 'fg:#858585 italic')    # disabled choices for select and checkbox prompts
])


# Classes

@dataclass
class YAMLKeyValuePair:
    key: str
    prompt_text: str
    value: str
    indent_level: int
    regex_pattern: str | Pattern
    hint: str
    required: bool
    comment: str
    active: bool = False


@dataclass
class YAMLDictionary:
    key: str
    value: str


@dataclass
class SocialLink:
    name: str
    icon: str
    link: str
    applied: bool


@dataclass
class Feature:
    id: str
    explanation: str
    active: bool


@dataclass
class CSS_COLOR:
    key: str
    value: str
    commented_out: bool
    comment: str


# Defaults
TEMPLATE_PATH = Path(os_path_abspath(__file__)).parent / "template"
DEFAULT_NAME = "docs"
CONFIG_FILE = Path("mkdocs.yml")
CSS_FILE = Path("pages") / "_internal" / "stylesheets" / "extra.css"
DEFAULT_QMARK = "?"
INDENTS = 2
SOCIAL_LINK_REQUIRED_FIELDS = ["name", "link", "icon"]


# Helpers

url_regex = compile(
    r"(\w+://)?"                # protocol                      (optional)
    r"(\w+\.)?"                 # host                          (optional)
    r"(([\w-]+)\.(\w+))"        # domain
    r"(\.\w+)*"                 # top-level domain              (optional, can have > 1)
    r"([\w\-\._\~/]*)*(?<!\.)"  # path, params, anchors, etc.   (optional)
)
url_regex_with_scheme = compile(
    r"(https?://)"              # protocol (http or https)    (required)
    r"(\w+\.)?"                 # host                         (optional)
    r"(([\w-]+)\.(\w+))"        # domain
    r"(\.\w+)*"                 # top-level domain             (optional, can have > 1)
    r"([\w\-\._\~/]*)*(?<!\.)"  # path, params, anchors, etc.  (optional)
)


# Data

PROJECT_DETAILS = [
    YAMLKeyValuePair(key="site_name",
                     prompt_text="Project name",
                     value="",
                     indent_level=0,
                     regex_pattern=None,
                     hint=None,
                     required=True,
                     comment=None),
    YAMLKeyValuePair(key="site_author",
                     prompt_text="Author(s)",
                     value="",
                     indent_level=0,
                     regex_pattern=None,
                     hint=None,
                     required=False,
                     comment=None),
    YAMLKeyValuePair(key="site_description",
                     prompt_text="Description",
                     value="",
                     indent_level=0,
                     regex_pattern=None,
                     hint=None,
                     required=False,
                     comment=None),
    YAMLKeyValuePair(key="copyright",
                     prompt_text="Footer text (e.g. copyright)",
                     value="Copyright &copy; <date(s)> <author>",
                     indent_level=0,
                     regex_pattern=None,
                     hint=None,
                     required=False,
                     comment=None),
    YAMLKeyValuePair(key="version",
                     prompt_text="Version",
                     value="",
                     indent_level=1,
                     regex_pattern=None,
                     hint=None,
                     required=False,
                     comment=None),
    YAMLKeyValuePair(key="site_url",
                     prompt_text="Hosted site url (empty if not hosted)",
                     value="",
                     indent_level=0,
                     regex_pattern=url_regex_with_scheme,
                     hint="If non-empty, it needs to be a valid URL with scheme",
                     required=False,
                     comment=None),
]
FAVICON = [YAMLKeyValuePair(key="favicon",
                            prompt_text="Favicon",
                            value="",
                            indent_level=1,
                            regex_pattern=None,
                            hint=None,
                            required=False,
                            comment=None)]
LOGOS = [YAMLKeyValuePair(key="logo",
                          prompt_text="Image logo",
                          value="",
                          indent_level=1,
                          regex_pattern=None,
                          hint=None,
                          required=False,
                          comment=None),
         YAMLKeyValuePair(key="logo",
                          prompt_text="Icon logo",
                          value="",
                          indent_level=2,
                          regex_pattern=None,
                          hint=None,
                          required=False,
                          comment=None)]
REPO_URL = [YAMLKeyValuePair(key="repo_url",
                             prompt_text="Repository url",
                             value="",
                             indent_level=0,
                             regex_pattern=url_regex_with_scheme,
                             hint="If non-empty, it needs to be a valid URL with scheme",
                             required=False,
                             comment=None)]


# Functions

def _find_file(file_name: str):
    """Find configuration file"""
    matches = [str(path) for path in Path(".").rglob(file_name)]
    if len(matches) == 1:
        return Path(matches[0])
    if len(matches) > 1:
        print(f"[Warning] Found multiple matching files")
        return Path(questionary_select("Correct config file", choices=matches, qmark=DEFAULT_QMARK, style=custom_style, use_arrow_keys=True, use_jk_keys=True, instruction="(Use arrow keys or j/k to move)").unsafe_ask())
    elif matches < 1:
        print("[Error] Configuration file not found")
        exit(1)


def _copy_template(destination_path: Path, overwrite: bool = True, only_config: bool = False) -> Path:
    f"""Copy template to destination directory.

    Args:
        destination_path (Path): Where to place documentation directory.
        overwrite (bool, optional): Whether to overwrite. Defaults to True.

    Returns:
        Path: Path to newly created directory.
    """

    # Check that template exists
    if not os_path_exists(TEMPLATE_PATH):
        print("\n[Error] Can't find template!")
        exit(1)

    # Check if destination path exists
    exists = os_path_exists(destination_path)

    # Overwrite or abort
    if exists:
        if overwrite:
            if only_config:
                if os_path_exists(destination_path / CONFIG_FILE):
                    remove(destination_path / CONFIG_FILE)
                if os_path_exists(destination_path / "pages" / "_internal"):
                    rmtree(destination_path / "pages" / "_internal")
            else:
                rmtree(destination_path)
        else:
            print("\nAborted")
            exit(1)

    # Copy selected template to destination
    if only_config:
        # Make directory
        (destination_path / "pages").mkdir(parents=True, exist_ok=True)
        # Copy only config and pages/_internal
        copy(TEMPLATE_PATH / CONFIG_FILE, destination_path / CONFIG_FILE)
        copytree(TEMPLATE_PATH / "pages" / "_internal", destination_path / "pages" / "_internal")
    else:
        copytree(TEMPLATE_PATH, destination_path)

    return destination_path


def _check_if_existing_directory(destination_path: Path, name: str):
    """Check if the project exists on path already"""

    # Set directory name if defined or not in path
    if name:
        if destination_path.name != name:
            destination_path = destination_path / name
    elif destination_path.name != DEFAULT_NAME:
        destination_path = destination_path / DEFAULT_NAME

    return destination_path, os_path_exists(destination_path)


def _get_project_name(file_path: Path):
    """Get the name of the project"""
    # Get file content
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    # Get site_name
    regex = compile(r"^\s*#?\s*site_name:\s*.*$", MULTILINE)
    # Get value, strip enclosing quotation marks, and do not split on ":" in value (just remove key)
    return ":".join(regex.findall(content)[0].split(":")[1:]).strip().strip("\"")


def prompt_for_key_values(fields: List[YAMLKeyValuePair]):
    for field in fields:
        while True:
            user_input = questionary_text(message=f"{field.prompt_text}:", default=field.value, qmark=DEFAULT_QMARK, style=custom_style).unsafe_ask()
            if field.required and user_input.strip() == "":
                print("This field is required, and cannot be empty!")
                continue
            if field.regex_pattern:
                regex_match = bool(match(field.regex_pattern, user_input))
                if user_input.strip() != "" and not regex_match:
                    print(f"\n{field.hint}\n")
                    continue
            field.value = f'''"{user_input}"'''
            break

    return fields


def write_key_values(file_path: Path, fields: List[YAMLKeyValuePair], indent_sensitive: bool = True, comment_out_inactive: bool = False):
    # Get file content
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    # Replace values per field
    for field in fields:
        # Find row based on regex
        if indent_sensitive:
            indent = " " * (INDENTS * field.indent_level)
            regex = compile(rf"^{indent}\s*#?\s*{field.key}:\s*.*$", MULTILINE)
        else:
            regex = compile(rf"^\s*#?\s*{field.key}:\s*.*$", MULTILINE)
        # We want to comment out empty fields (if not required), and uncomment non-empty fields
        if ("#" in field.key and (field.required or field.value.strip() not in ['', '""'])):
            field.key = field.key.strip("#").strip()
        if (field.value.strip() in ['', '""'] and not field.required) or (comment_out_inactive and not field.active):
            field.key = "# " + field.key
        # Substitute content with indents
        content = regex.sub(f"{' ' * INDENTS * field.indent_level}{field.key}: {field.value}{' # ' + field.comment if field.comment else ''}", content, count=1)
    # Overwrite file content
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def _is_comment(line: str):
    first_non_space = search(r"\S", line)
    if first_non_space:
        return line[first_non_space.start()] == "#"
    return False


def _get_values_of_fields_in_file(file_path: Path, fields: List[YAMLKeyValuePair], indent_sensitive: bool = True):
    # Get file content
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    # Find values in content
    for field in fields:
        # Find value, strip enclosing quotation marks, and do not split on ":" in value (just remove key)
        if indent_sensitive:
            indent = " " * (INDENTS * field.indent_level)
            regex = compile(rf"^{indent}\s*#?\s*{field.key}:\s*.*$", MULTILINE)
        else:
            regex = compile(rf"^\s*#?\s*{field.key}:\s*.*$", MULTILINE)
        found_rows = regex.findall(content)
        if len(found_rows) != 0:
            row = found_rows[0]
            field.value = "".join(":".join(row.split(":")[1:]).split("#")[0]).strip().strip("\"")
            field.active = _is_comment(row) == False
            # Find comment (not whole line, only inline after text)
            regex = compile(r"(?<=\S).*(#.*)$", MULTILINE)
            found_comments = regex.findall(row)
            if len(found_comments) != 0:
                comment = found_comments
                field.comment = comment[0].strip("#").strip()
    return fields


def _find_repo_name_suggestion(text: str):

    # Regular expression pattern
    pattern = r"https?:\/\/(?:www\.)?(?:github\.com|gitlab\.com|bitbucket\.org)\/([^\/]+)\/([^\/?#]+)"

    # Find matches
    regex_match = search(pattern, text.strip('').strip('"'))

    # Return "account/repo" if match, else ""
    if regex_match:
        # Manually remove the '.git' extension if present
        repo_name = regex_match.group(2).removesuffix('.git')
        account_repo = regex_match.group(1) + "/" + repo_name
        return account_repo
    else:
        return ""


def _extract_css_variables(css, scheme) -> List[CSS_COLOR]:
    # Adjust the pattern to include both uncommented and commented-out variables
    pattern = rf'\[data-md-color-scheme="{scheme}"\] > \*\s*\{{(.*?)\}}'
    block_match = search(pattern, css, DOTALL)

    if not block_match:
        return []

    variables_block = block_match.group(1)
    # This regex now captures commented-out variables and their inline comments
    var_pattern = r'(?:(/\*\s*)?(\s*--[^:]+):\s*([^;]+);\s*(?:\*/\s*)?(?:(/\*[^*]*\*/))?)'
    matches = findall(var_pattern, variables_block)

    variables = [
        CSS_COLOR(key=match[1].strip(),
                  value=match[2].strip(),
                  commented_out=True if match[0].strip() else False,
                  comment=(match[3].strip()[2:-2] if match[0].strip() else match[3].strip()[2:-2]).strip() if match[3].strip() else None)
        for match in matches
    ]
    return variables


def _update_css_variables(file_path: str, scheme: str, updated_vars: List[CSS_COLOR]):
    """Function for overwriting css variables, with regex finetuned for color selection inside "[data-md-color-scheme="default"] > * { ... }"

    Args:
        file_path (str): Stylesheet path
        scheme (str): Name of color scheme
        updated_vars (List[CSS_COLOR]): List of vars to be updated
    """
    with open(file_path, 'r') as css_file:
        css_content = css_file.read()

    # Find the scheme block within the CSS content
    scheme_pattern = compile(r'(\[data-md-color-scheme="' + escape(scheme) + r'"\] > \*\s*\{)(.*?)(\}\s*?)', DOTALL)
    match = scheme_pattern.search(css_content)

    if not match:
        return  # Scheme block not found, exit function

    # Find the scheme block, and prepare for updating
    scheme_block = match.group(2)
    updated_scheme_block = ""

    # Go through line for line
    for line in scheme_block.splitlines(keepends=False):
        updated_line = line
        # For variable in the list of variables to update
        for var in updated_vars:
            # Pattern to match both active and commented versions of the variable
            var_pattern = compile(rf'^(\s*)(/\*)? ?{escape(var.key)}\s*:\s*[^;]+; ?(\*/)?(.*)$', DOTALL)
            match_var = var_pattern.match(line)
            if match_var:
                # Construct the new line based on whether it's commented out
                prefix = match_var.group(1)  # Preserve leading spaces for indentation
                inline_comment = match_var.group(4)  # Preserve any inline comment

                if var.commented_out:
                    updated_line = f"{prefix}/* {var.key}: {var.value}; */ {inline_comment.lstrip()}"
                else:
                    updated_line = f"{prefix}{var.key}: {var.value}; {inline_comment.lstrip()}"
                break  # Stop checking once the first match is found and updated
        updated_scheme_block += updated_line + "\n"

    # Reconstruct the full CSS content with the updated scheme block
    updated_css_content = css_content[:match.start(2)] + updated_scheme_block.rstrip() + "\n" + css_content[match.end(2):]

    # Write to file
    with open(file_path, 'w') as css_file:
        css_file.write(updated_css_content)


def extract_features(yaml_content: str) -> List[Feature]:
    """Extract features from the config file"""

    # Regex
    features_key_re = compile(r"^\s*features:\s*$")
    feature_line_re = compile(r"^\s*#*\s*- ([\w.]+)(?:\s*#\s*(.*))?$")
    indent_re = compile(r"^(\s*)")
    comment_re = compile(r"^\s*#")

    # Iterate line by line
    lines = yaml_content.splitlines()

    features = []
    in_features_section = False
    features_indent = 0
    for line in lines:
        # Skip lines not being a list entry
        if "- " in line or "features" in line:
            if features_key_re.match(line):
                in_features_section = True
                features_indent = len(indent_re.match(line).group(1))
                continue

            current_indent = len(indent_re.match(line).group(1))
            if in_features_section and (not line.strip() or current_indent <= features_indent):
                break

            if in_features_section:
                match = feature_line_re.match(line)
                if match:
                    feature_id, explanation = match.groups()
                    # Determine if the feature is active based on whether the first non-space character is '#'
                    active = not comment_re.match(line[current_indent:])
                    features.append(Feature(id=feature_id, explanation=explanation or feature_id, active=active))

    return features


def write_features(features: List[Feature], config_path: Path):
    """Write features to config file"""

    # Read yaml file
    with open(config_path, 'r') as file:
        yaml_lines = file.readlines()

    # Replace line content if feature id in line
    for feature in features:
        for i, line in enumerate(yaml_lines):
            if feature.id in line.strip().split(" "):
                yaml_lines[i] = f"{' ' * INDENTS * 2}{'' if feature.active else '# '}- {feature.id}{' # ' + feature.explanation if feature.explanation else ''}\n"

    # Write lines back again
    with open(config_path, 'w') as file:
        yaml_lines = file.writelines(yaml_lines)


def cli():
    """A command line interface for initializing a MkDocs project"""
    # Arguments
    # Add a suitable description for your tool
    parser = ArgumentParser(description='Command Line Interface to create and update mkdocs documentation projects.')
    parser.add_argument('-p', '--path', type=Path, default=None, help='documentation directory, prompted if not set')
    parser.add_argument('-d', '--dir-name', type=str, default=None, help='name of the directory, if not default "docs"')
    parser.add_argument('--print-config', action=BooleanOptionalAction, help='print the content of "mkdocs.yml" and exit')
    args = parser.parse_args()

    # Run main function
    main(path=args.path, dir_name=args.dir_name, print_config=args.print_config)


# Main
def main(path: Path, dir_name: str, print_config: bool):
    """The main flow of the initdocs program"""
    print("\nWelcome to InitDocs!")

    # Ask for path if not given
    if not path:
        print("")
        path = Path(questionary_path("Docs parent directory (default: cwd)", only_directories=True,
                    default=getcwd(), qmark=DEFAULT_QMARK, style=custom_style).unsafe_ask())

    # Check if exists already
    directory_path, exists = _check_if_existing_directory(destination_path=path, name=dir_name)
    config_path = directory_path / CONFIG_FILE
    css_file_path = directory_path / CSS_FILE
    yaml = YAML(typ=['rt', 'string'])

    if print_config:
        print("")
        if exists and os_path_exists(directory_path / CONFIG_FILE.name):
            print("> Printing configuration\n")
            content = open(config_path, "r").read()
            print(content)
        else:
            print("No documentation project found.")
        exit(0)

    # Initialize project if not exists
    if exists and os_path_exists(directory_path / CONFIG_FILE.name):
        print(f"\nFound an existing project. Making changes to the docs \"{_get_project_name(config_path)}\".")
    else:

        # Decide whether to overwrite all, or just config file and _internal
        # Defaults to full initialization
        # TODO should overwrite everything except pages folder
        overwrite_pages = "Full initialization"
        if exists:
            print("")
            overwrite = questionary_confirm(message=f"[Warning] A directory seems to exist at '{directory_path}', but it is not a complete MkDocs project. Do you want to overwrite?",
                                                    default=False, auto_enter=False, qmark=DEFAULT_QMARK, style=custom_style).unsafe_ask()
            # Abort if not confirmed
            if not overwrite:
                print("\nAborted")
                exit(0)

            print("")
            if os_path_exists(directory_path / CONFIG_FILE.name):
                overwrite_pages = questionary_select("Do you want to keep current pages, or initialize the project from scratch?",
                                                     choices=["Keep my current documentation", "Full initialization"],
                                                     qmark=DEFAULT_QMARK, style=custom_style, use_arrow_keys=True, use_jk_keys=True,
                                                     instruction="(Use arrow keys or j/k to move)").unsafe_ask()
            else:
                rmtree(directory_path)

        # Prompt for metadata, before copying template and writing key values
        print(f"\n> Initializing from template in directory '{directory_path.name}'\n")
        metadata = prompt_for_key_values(PROJECT_DETAILS)

        # Copy template
        _copy_template(destination_path=directory_path, overwrite=True, only_config=overwrite_pages == "Keep my current documentation")

        # Write metadata
        write_key_values(file_path=directory_path / CONFIG_FILE, fields=metadata)

        # Done
        print(f"\nSuccessfully initialized docs!")

        # Should exit on first initialization
        exit(0)

    # Action checkbox
    print("")
    update_choices = ["Update project details", "Repository card", "Theme colors",
                      "Social links", "Features", "Icon/logo", "Reset"]
    try:
        what_to_configure = questionary_checkbox("What do you want to configure?" if exists else "Do you want to configure more?",
                                                 choices=update_choices, qmark=DEFAULT_QMARK, style=custom_style,
                                                 use_arrow_keys=True, use_jk_keys=True,
                                                 instruction="(Use arrow keys or j/k to move, <space> to select, <a> to toggle all, <i> to invert)").unsafe_ask()

        # If reinitialize together with other actions, we should reinitialize first
        if "Reset" in what_to_configure and len(what_to_configure) > 1:
            what_to_configure = ["Reset"] + [action for action in what_to_configure if action not in ["Reset"]]

    except KeyboardInterrupt:
        print("\nDone")
        exit(0)

    # Perform action
    for i, choice in enumerate(what_to_configure):
        match choice:
            case "Update project details":
                print(f"\n> (Step {i + 1}/{len(what_to_configure)}) Updating project details\n")
                # Prompt for metadata with existing values as defaults
                metadata = prompt_for_key_values(_get_values_of_fields_in_file(file_path=config_path, fields=PROJECT_DETAILS))
                # Write metadata
                write_key_values(file_path=config_path, fields=metadata)
                # Done
                print("\nSuccessfully updated docs!")

            case "Repository card":
                print(f"\n> (Step {i + 1}/{len(what_to_configure)}) Configuring link to repository\n")
                print("If configured, a repository card will be rendered in the navbar (desktop) or sidebar (mobile).\n")

                # Prompt for repourl with existing values as defaults
                repo_url = prompt_for_key_values(_get_values_of_fields_in_file(file_path=config_path, fields=REPO_URL))[0]

                # We want to prompt reponame. First, check current value and infer from url if empty.
                repo_name_in_config = _get_values_of_fields_in_file(file_path=config_path, fields=[
                    YAMLKeyValuePair(key="repo_name",
                                     prompt_text="Repository name",
                                     value="",
                                     indent_level=0,
                                     regex_pattern=None,
                                     hint=None,
                                     required=False,
                                     comment=None),
                ])[0]
                # If empty, infer from url instead
                if repo_name_in_config.value.strip("") in ['', '""']:
                    repo_name_in_config.value = _find_repo_name_suggestion(repo_url.value)
                repo_name = prompt_for_key_values(fields=[repo_name_in_config])[0]
                # Write metadata
                repository_fields = [repo_url, repo_name]
                write_key_values(file_path=config_path, fields=repository_fields)

                # Done
                print("\nSuccessfully updated social card settings!")

            case "Theme colors":
                print(f"\n> (Step {i + 1}/{len(what_to_configure)}) Theme colors\n")

                # What color scheme to alter
                schemes_to_alter = questionary_checkbox("Which color schemes will you alter?",
                                                        choices=["Light", "Dark"], qmark=DEFAULT_QMARK, style=custom_style,
                                                        use_arrow_keys=True, use_jk_keys=True,
                                                        instruction="(Use arrow keys or j/k to move, <space> to select, <a> to toggle all, <i> to invert)").unsafe_ask()

                # If nothing to alter, skip
                if len(schemes_to_alter) == 0:
                    break

                # Extract css contents
                css_content = open(css_file_path, "r").read()

                # Iterate over selected schemes
                for scheme in schemes_to_alter:
                    # Extract current variables
                    list_of_css_colors = _extract_css_variables(css_content, "default" if scheme == "Light" else "slate")
                    # Prompt for new values
                    yaml_key_value_pairs = [YAMLKeyValuePair(color.key, f"{color.key} ({color.comment})", color.value, 1, None, color.comment,
                                                             True, None) for color in list_of_css_colors if not color.commented_out]
                    metadata = prompt_for_key_values(yaml_key_value_pairs)
                    # Simplify to key value dict
                    new_key_values = dict()
                    for key_pair in metadata:
                        new_key_values[key_pair.key] = key_pair.value.strip("\"")
                    # Find the ones that we have changed
                    updated_variables = [CSS_COLOR(color.key, new_key_values[color.key], False, None)
                                         for color in list_of_css_colors if not color.commented_out and color.value != new_key_values[color.key]]
                    # Make changes to file
                    _update_css_variables(css_file_path, "default" if scheme == "Light" else "slate", updated_variables)

                    # Print a message
                    print(f"\nSuccessfully updated {len(updated_variables)} color variable{'s' if len(updated_variables) > 1 else ''}!"
                          if len(updated_variables) != 0 else "\nNo changes made")

            case "Social links":
                print(f"\n> (Step {i + 1}/{len(what_to_configure)}) Social links")

                print(f"Description: In the footer, one can display a collection of social media links, defined as a list of dictionaries under extra/social in the config file.\n")

                # Map social link name and icons
                social_links_name_icon_map = {
                    "GitHub": "fontawesome/brands/github",
                    "Docker": "fontawesome/brands/docker",
                    "LinkedIn": "fontawesome/brands/linkedin",
                    "Twitter": "fontawesome/brands/x-twitter",
                    "YouTube": "fontawesome/brands/youtube",
                    "Discord": "fontawesome/brands/discord",
                    "StackOverflow": "fontawesome/brands/stack-overflow",
                    "DEV": "fontawesome/brands/dev",
                    "Medium": "fontawesome/brands/medium",
                    "Slack": "fontawesome/brands/slack",
                    "Facebook": "fontawesome/brands/facebook",
                    "Instagram": "fontawesome/brands/instagram",
                    "TikTok": "fontawesome/brands/tiktok",
                    "Mastodon": "fontawesome/brands/mastodon",
                    "Webpage": "fontawesome/brands/globe",
                }

                # Generate options
                social_link_options: Dict[str, SocialLink] = {}
                for key, value in social_links_name_icon_map.items():
                    social_link_options[key] = SocialLink(name=key, icon=value, link="", applied=False)
                social_link_options["Other"] = SocialLink(name="Other", link="", icon="", applied=False)

                # Read config file
                try:
                    with open(config_path, 'r') as config_file:
                        yaml_object = yaml.load(config_file)
                    # Ensure not none, rather empty list
                    if yaml_object["extra"]["social"] is None:
                        yaml_object["extra"]["social"] = []
                    social_yaml = yaml_object["extra"]["social"]
                except KeyError:
                    print("[Error] Could not find the key 'social' inside 'extra', please insert again!")
                    exit(1)
                except TypeError:
                    print("[Error] Could not find the key 'social' inside 'extra', please insert again!")
                    exit(1)
                except ScannerError:
                    print("[Error] Illegal YAML format (might be missing a colon somewhere), please revert your changes!")
                    exit(1)
                except ParserError:
                    print("[Error] Illegal YAML format (might be the indentation), please revert your changes!")
                    exit(1)

                # Update options based on config file
                name_counts = defaultdict(int)
                not_complete_elements = []
                for element in social_yaml:
                    if all(key in element for key in SOCIAL_LINK_REQUIRED_FIELDS):
                        name_counts[element["name"]] += 1
                        social_link_options[element["name"]] = SocialLink(name=element["name"], icon=element["icon"], link=element["link"], applied=True)
                    else:
                        not_complete_elements.append(element)

                # Ensure all elements has all required fields
                if len(not_complete_elements) > 0:
                    print("[Error] Found incomplete social link entries!")
                    print(f"Config path: {config_path}")
                    print(f"Required fields: {SOCIAL_LINK_REQUIRED_FIELDS}\n")

                    print(f"Incomplete entries:")
                    for element in not_complete_elements:
                        missing_fields = [key for key in SOCIAL_LINK_REQUIRED_FIELDS if key not in element.keys()]
                        print(f"{element} is missing field{'s' if len(missing_fields) > 1 else ''}: {missing_fields}")
                    print(f"\nTo continue, please ensure all entries include the required fields")
                    exit(0)

                # Ensure no duplicate names
                duplicate_names = [name for name, count in name_counts.items() if count > 1]
                if len(duplicate_names) > 0:
                    print("[Error] Found duplicates social link entries!")
                    print(f"Config path: {config_path}")
                    print(f"Duplicate entries: {duplicate_names}")
                    print(f"\nPlease replace the duplicated entries with unique names")
                    exit(0)

                # Ask user for links
                choices: Dict[str, SocialLink] = questionary_checkbox("Which links do you want to display in the footer?",
                                                                      choices=[questionary_choice(social.name, social, checked=social.applied)
                                                                               for social in social_link_options.values()],
                                                                      qmark=DEFAULT_QMARK, use_arrow_keys=True, use_jk_keys=True,
                                                                      style=custom_style).unsafe_ask()

                # Find length of applied vs length of choices
                n_already_applied = sum(1 for social_link in social_link_options.values() if social_link.applied)
                n_choices = len([choice for choice in choices if choice.name != "Other"])
                if n_choices < n_already_applied:
                    whether_to_continue = questionary_confirm(message=f"[Warning] You have selected to keep {n_choices} of {n_already_applied} social links, and the unselected will be deleted. Continue?", default=False,
                                                              auto_enter=False, qmark=DEFAULT_QMARK, style=custom_style).unsafe_ask()
                    if whether_to_continue:
                        # Unapply all not checked
                        to_be_unapplied = [obj for obj in social_link_options.values() if obj.applied and obj not in choices]
                        for obj in to_be_unapplied:
                            social_link_options[obj.name].applied = False
                    else:
                        print("Aborted")
                        exit(0)

                # Prompting for information per social account
                for choice in choices:
                    # Get key
                    choice_key = choice.name

                    # Add if other, update if pre-existing key
                    if choice_key == "Other":
                        while True:
                            print(f"\nNew entry")
                            # Name
                            input_name = questionary_text(
                                f"Name:",
                                validate=lambda input_str:
                                    "This entry exists, select from list" if input_str.lower() in (key.lower() for key in social_link_options) else
                                    "Cannot be empty" if input_str.strip() == ""
                                    else True,
                                qmark=DEFAULT_QMARK,
                                style=custom_style,
                            ).unsafe_ask()

                            # Link
                            input_link = questionary_text(
                                f"Link",
                                validate=lambda input_str:
                                    "Invalid URL format" if not url_regex.match(input_str) is not None else
                                    "Cannot be empty" if input_str.strip() == ""
                                    else True,
                                qmark=DEFAULT_QMARK,
                                style=custom_style
                            ).unsafe_ask()

                            # Option
                            input_icon = questionary_text(
                                f"Icon",
                                validate=lambda input_str:
                                    "Cannot be empty" if input_str.strip() == ""
                                    else True,
                                qmark=DEFAULT_QMARK,
                                style=custom_style
                            ).unsafe_ask()

                            social_link_options[input_name] = SocialLink(name=input_name, icon=input_icon, link=input_link, applied=True)

                            # Prompt for another?
                            another = questionary_confirm(message="\nAdd other entries?", default=False,
                                                          auto_enter=False, qmark=DEFAULT_QMARK, style=custom_style).unsafe_ask()
                            if not another:
                                break
                    else:
                        print(f"\n{choice_key}")

                        # Set link
                        input_link = questionary_text(
                            f"Link",
                            validate=lambda url: "Invalid URL format" if not url_regex.match(url) is not None else True,
                            default=social_link_options[choice_key].link,
                            qmark=DEFAULT_QMARK,
                            style=custom_style
                        ).unsafe_ask()

                        social_link_options[choice_key].link = input_link

                        # Update icon?
                        update_icon = questionary_confirm(message="Do you want to change icon?", default=False,
                                                          auto_enter=False, qmark=DEFAULT_QMARK, style=custom_style).unsafe_ask()
                        if update_icon:
                            input_icon = questionary_text(
                                f"Icon",
                                default=social_link_options[choice_key].icon,
                                qmark=DEFAULT_QMARK,
                                style=custom_style
                            ).unsafe_ask()
                            social_link_options[choice_key].icon = input_icon

                        # Set applied
                        social_link_options[choice_key].applied = True

                # Alter social yaml object
                # exit(0)
                for key, value in social_link_options.items():
                    match_indices = [index for index, d in enumerate(social_yaml) if d.get("name") == value.name]
                    if value.applied:
                        if len(match_indices) > 0:
                            for match_i in match_indices:
                                social_yaml[match_i] = {"name": value.name, "icon": value.icon, "link": value.link}
                        else:
                            social_yaml.append({"name": value.name, "icon": value.icon, "link": value.link})
                    else:
                        for match_i in match_indices:
                            social_yaml.pop(match_i)

                # Write file
                with open(config_path, 'w') as yaml_file:
                    yaml.dump(yaml_object, yaml_file)

                print(f"\nSuccessfully updated social links!")

            case "Features":
                print(f"\n> (Step {i + 1}/{len(what_to_configure)}) Selectable features\n")

                # Extract features
                file_str = open(config_path).read()
                features = extract_features(file_str)

                # Prompt user
                user_answer = questionary_checkbox("Which features do you want to keep?",
                                                   choices=[questionary_choice(title=feature.explanation, value=feature.id,
                                                                               checked=feature.active) for feature in features],
                                                   qmark=DEFAULT_QMARK, use_arrow_keys=True, use_jk_keys=True,
                                                   style=custom_style).unsafe_ask()

                # Update the active value based on user answer
                for feature in features:
                    feature.active = feature.id in user_answer

                write_features(features, config_path)

            case "Icon/logo":
                print(f"\n> (Step {i + 1}/{len(what_to_configure)}) Icon & logo\n")

                # Get new value for favicon
                icon = prompt_for_key_values(_get_values_of_fields_in_file(config_path, FAVICON))

                # Logo can have two alternatives. So (1) find current, ask if what type, and prompt for value for correct type
                logo_values = _get_values_of_fields_in_file(config_path, LOGOS)
                active = [logo.prompt_text for logo in logo_values if logo.active]
                if len(active) == 0:
                    print("\nYou need to define a logo, which format do you prefer?")
                elif len(active) == 2:
                    print("\nYou can only have one active logo!")
                else:
                    print(f"\nYou are currently using an {active[0].lower()}. Do you want to keep the same format, or switch?")
                new_logo_type = questionary_select("Icon", choices=[questionary_choice(title=logo.prompt_text, value=logo.prompt_text,
                                                                                       checked=False) for logo in logo_values],
                                                   qmark=DEFAULT_QMARK, style=custom_style, use_arrow_keys=True, use_jk_keys=True,
                                                   instruction="(Use arrow keys or j/k to move)").unsafe_ask()
                # Make only new logo type active
                for logo in logo_values:
                    logo.active = new_logo_type == logo.prompt_text
                    if logo.active:
                        logo = prompt_for_key_values([logo])[0]

                write_key_values(config_path, icon + logo_values, comment_out_inactive=True)

                # Done
                print(f"\nSuccessfully updated icon and logo!")

            case "Reset":

                print(f"\n> (Step {i + 1}/{len(what_to_configure)}) Reset project\n")

                # Decide on resetting configuration or whole project
                action = questionary_select("Choose an action", choices=["Reset configuration", "Reinitialize clean project"],
                                            qmark=DEFAULT_QMARK, style=custom_style, use_arrow_keys=True, use_jk_keys=True,
                                            instruction="(Use arrow keys or j/k to move)").unsafe_ask()

                if action == "Reset configuration":
                    print("")
                    overwrite = questionary_confirm(message="[Warning] This will overwrite the 'mkdocs.yml' and 'pages/_internal'. Are you sure?",
                                                    default=False, auto_enter=False, qmark=DEFAULT_QMARK, style=custom_style).unsafe_ask()

                    # Abort if not confirmed
                    if not overwrite:
                        print("\nAborted")
                        exit(0)

                if action == "Reinitialize clean project":
                    print("")
                    overwrite = questionary_confirm(message="[Warning] You are about to overwrite the entire directory, instead of updating the metadata. Are you sure?",
                                                    default=False, auto_enter=False, qmark=DEFAULT_QMARK, style=custom_style).unsafe_ask()

                    # Abort if not confirmed
                    if not overwrite:
                        print("\nAborted")
                        exit(0)

                # Get metadata
                print("")
                action = questionary_select("Choose an action", choices=["Reinitialize project details", "Alter existing project details"],
                                            qmark=DEFAULT_QMARK, style=custom_style, use_arrow_keys=True, use_jk_keys=True,
                                            instruction="(Use arrow keys or j/k to move)").unsafe_ask()
                print("")
                if action == "Alter existing project details":
                    metadata = prompt_for_key_values(_get_values_of_fields_in_file(file_path=config_path, fields=PROJECT_DETAILS))
                else:
                    metadata = prompt_for_key_values(PROJECT_DETAILS)

                # Write metadata
                _copy_template(destination_path=directory_path, overwrite=True, only_config=action == "Reset configuration")
                write_key_values(file_path=directory_path / CONFIG_FILE, fields=metadata)

                # Done
                print(f"\nSuccessfully reinitialized docs!")

            case _:
                pass


if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt:
        print("\nInterrupted")
        exit(0)
