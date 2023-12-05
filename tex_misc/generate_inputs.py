import os
import yaml


def get_folders(path: str) -> list[str]:
    # Get a list of all items (files and folders) in the specified path
    items = os.listdir(path)
    # Filter out only the folders
    folders = [item for item in items if os.path.isdir(
        os.path.join(path, item))]
    return folders


def build_chapter_tex_file(chapter: str) -> None:
    # Get nice names for chapters
    with open("config.yaml", "r") as yaml_file:
        chapter_mappings = yaml.safe_load(yaml_file)["chapter_mappings"]

    # Input all the contents for the current chapter
    chapter_name = chapter_mappings[chapter] if chapter in list(
        chapter_mappings.keys()) else chapter
    tex_content = f"\\chapter{{{chapter_name}}}\n\n"
    for x in os.listdir(f"../chapters/{chapter}"):
        tex_content += f"\\input{{chapters/{chapter}/{x}}}\n"

    with open(f"../chapters/{chapter}.tex", "w") as tex_file:
        tex_file.write(tex_content)


def build_inputs() -> None:
    tex_content = ""
    for chap in get_folders("../chapters/"):
        tex_content += f"\\input{{chapters/{chap}}}\n"

    with open("inputs.tex", "w") as tex_file:
        tex_file.write(tex_content)


if __name__ == "__main__":
    for chap in get_folders("../chapters/"):
        build_chapter_tex_file(chap)
    build_inputs()
