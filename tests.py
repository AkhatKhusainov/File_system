from datetime import datetime, timedelta

from src import Directory, File


def build_sample_tree() -> Directory:
    root = Directory("root")
    docs = Directory("docs")
    img = Directory("img")
    readme = File("readme.md", 100)
    guide = File("guide.txt", 50)
    logo = File("logo.png", 2000)

    docs.add(readme)
    docs.add(guide)
    img.add(logo)
    root.add(docs)
    root.add(img)
    return root


def test_modified_at_updates_on_add():
    root = Directory("root")
    before = root.modified_at
    f = File("a.txt", 10)
    root.add(f)
    assert root.modified_at >= before


def test_list_paths_returns_all_paths():
    root = build_sample_tree()
    paths = sorted(root.list_paths())
    assert paths == [
        "root/docs/guide.txt",
        "root/docs/readme.md",
        "root/img/logo.png",
    ]


def test_tree_contains_names_and_sizes():
    root = build_sample_tree()
    tree_str = root.tree()
    assert "root/ (" in tree_str
    assert "docs/ (" in tree_str
    assert "img/ (" in tree_str
    assert "readme.md (100 B)" in tree_str
    assert "guide.txt (50 B)" in tree_str
    assert "logo.png (2000 B)" in tree_str


def test_to_dict_recursive():
    root = build_sample_tree()
    d = root.to_dict()
    assert d["type"] == "dir"
    assert d["name"] == "root"
    assert isinstance(d["children"], list)
    # find nested file dicts
    names = []
    def collect(node_dict):
        if node_dict["type"] == "file":
            names.append(node_dict["name"])
        else:
            for ch in node_dict["children"]:
                collect(ch)
    collect(d)
    assert set(names) == {"readme.md", "guide.txt", "logo.png"}


def test_no_bonus_methods():
    root = build_sample_tree()
    # Directory should not expose bonus APIs in this simplified version
    assert not hasattr(root, "find")
    assert not hasattr(root, "remove")


def test_file_modify_updates_size_and_mtime():
    f = File("a.txt", 10)
    before = f.modified_at
    f.modify(20)
    assert f.size() == 20
    assert f.modified_at >= before


def run_all():
    test_modified_at_updates_on_add()
    test_list_paths_returns_all_paths()
    test_tree_contains_names_and_sizes()
    test_to_dict_recursive()
    test_no_bonus_methods()
    test_file_modify_updates_size_and_mtime()
    print("All tests passed.")


if __name__ == "__main__":
    run_all()

