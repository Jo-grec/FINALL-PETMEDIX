import os
import shutil


def remove_path(target_path: str) -> None:
    """Remove a file or directory if it exists."""
    if os.path.isdir(target_path):
        shutil.rmtree(target_path, ignore_errors=True)
    elif os.path.isfile(target_path):
        try:
            os.remove(target_path)
        except OSError:
            pass


def remove_globbed_files(root: str, patterns: list[str]) -> None:
    """Remove files matching any of the glob patterns under root recursively."""
    import glob

    for pattern in patterns:
        for filepath in glob.glob(os.path.join(root, pattern), recursive=True):
            if os.path.isfile(filepath):
                try:
                    os.remove(filepath)
                except OSError:
                    pass


def ensure_gitkeep_dirs(directories: list[str]) -> None:
    """Create directories and place a .gitkeep so they stay tracked when empty."""
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        gitkeep = os.path.join(directory, ".gitkeep")
        if not os.path.exists(gitkeep):
            with open(gitkeep, "w", encoding="utf-8") as f:
                f.write("")


def main() -> None:
    # Remove build artifacts and packaged outputs
    for path in [
        "build",
        "dist",
        "PetMedix_20250523_094927",
    ]:
        remove_path(path)

    # Remove archives
    remove_globbed_files(".", ["*.zip", "*.tar", "*.tar.gz"])

    # Remove generated PDFs
    remove_globbed_files(
        ".",
        [
            "pdf_reports/*.pdf",
            "pdf_reports/**/*.pdf",
            "billing_pdf/*.pdf",
            "billing_pdf/**/*.pdf",
            "Invoice_*.pdf",
        ],
    )

    # Recreate expected output dirs with .gitkeep
    ensure_gitkeep_dirs(
        [
            "pdf_reports",
            "pdf_reports/appointments",
            "pdf_reports/invoices",
            "pdf_reports/reports",
            "billing_pdf",
            "profile_photos",
        ]
    )


if __name__ == "__main__":
    main()
