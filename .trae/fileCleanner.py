import os
import shutil


TEMP_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ipynb_checkpoints",
    ".cache",
}

TEMP_FILE_SUFFIXES = (
    ".pyc",
    ".pyo",
    ".pyd",
    ".pdb",
    ".swp",
    ".swo",
    ".tmp",
    ".temp",
    "~",
)

TEMP_FILE_NAMES = {
    ".DS_Store",
    ".localized",
}


def is_temp_dir(name: str) -> bool:
    return name in TEMP_DIR_NAMES


def is_temp_file(name: str) -> bool:
    return (
        name in TEMP_FILE_NAMES
        or name.startswith("._")
        or name.endswith(TEMP_FILE_SUFFIXES)
    )


def cleanup():
    """清理项目中的临时文件，包括 __pycache__、编译文件、Apple 隐藏文件等。"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    print(f"开始清理项目目录: {project_root}")

    count_dirs = 0
    count_files = 0

    for root, dirs, files in os.walk(project_root, topdown=False):
        for name in dirs:
            if is_temp_dir(name):
                dir_path = os.path.join(root, name)
                try:
                    shutil.rmtree(dir_path)
                    print(f"已删除目录: {dir_path}")
                    count_dirs += 1
                except Exception as e:
                    print(f"删除目录失败 {dir_path}: {e}")

        for name in files:
            if is_temp_file(name):
                file_path = os.path.join(root, name)
                try:
                    os.remove(file_path)
                    print(f"已删除文件: {file_path}")
                    count_files += 1
                except Exception as e:
                    print(f"删除文件失败 {file_path}: {e}")

    print("=" * 50)
    print(f"清理完成！共删除目录: {count_dirs} 个，文件: {count_files} 个")
    print("=" * 50)


if __name__ == "__main__":
    cleanup()
