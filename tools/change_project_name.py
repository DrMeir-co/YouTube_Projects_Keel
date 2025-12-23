from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
OLD = "juicy_tool_name"


def replace_in_file(
    path: Path, old: str, new: str, title_old: str, title_new: str, new_desc: str | None
):
    txt = path.read_text(encoding="utf-8")
    txt = txt.replace(old, new)
    txt = txt.replace(title_old, title_new)
    # If README.md, replace its first line with a heading containing the new name and description
    if path.name == "README.md":
        lines = txt.splitlines()
        if lines:
            lines[0] = (f"# {new} — {new_desc or ''}").title()
            txt = "\n".join(lines)
    if path.name == "pyproject.toml" and new_desc:
        lines = txt.splitlines()
        for i, ln in enumerate(lines):
            if ln.strip().startswith("description") and "=" in ln:
                lines[i] = f'description = "{new_desc}"'
                break
        txt = "\n".join(lines)
    path.write_text(txt, encoding="utf-8")


def main():
    new = desc = None
    while not new:
        new = input("New package name: ").strip()
    while not desc:
        desc = input("Short description for pyproject.toml: ").strip()

    title_old = "Juicy_Tool_Name"
    title_new = new.replace("-", "_").title().replace(" ", "_")

    files = [ROOT / "README.md", ROOT / "pyproject.toml"]
    for f in files:
        if f.exists():
            replace_in_file(f, OLD, new, title_old, title_new, desc or None)
            print(f"Updated {f.relative_to(ROOT)}")

    src_old = ROOT / "src" / OLD
    src_new = ROOT / "src" / new
    if not src_old.exists():
        print(f"Package directory {src_old} not found — nothing to rename.")
        return
    if src_new.exists():
        print(f"Target directory {src_new} already exists — aborting rename.")
        return
    shutil.move(str(src_old), str(src_new))
    print(f"Renamed package directory to src/{new}")


if __name__ == "__main__":
    main()
