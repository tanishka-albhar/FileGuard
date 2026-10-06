import os
import json
import hashlib


# Project folders and files
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(PROJECT_ROOT, "data")
BASELINE_FILE = os.path.join(DATA_FOLDER, "baseline.json")


def calculate_hash(file_path):
    """
    Calculate the SHA-256 hash of a file.
    """

    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while True:
                data = file.read(4096)

                if not data:
                    break

                sha256.update(data)

        return sha256.hexdigest()

    except PermissionError:
        print(f"[!] Permission denied: {file_path}")
        return None

    except OSError:
        print(f"[!] Could not read file: {file_path}")
        return None


def handle_walk_error(error):
    """
    Handle errors while scanning directories.
    """

    print(f"[!] Could not access directory: {error}")


def get_files(directory):
    """
    Find all files inside the selected directory.
    """

    files = []

    for root, directories, filenames in os.walk(
        directory,
        onerror=handle_walk_error
    ):
        for filename in filenames:

            file_path = os.path.join(root, filename)

            # Do not include the baseline file itself
            if os.path.abspath(file_path) == os.path.abspath(BASELINE_FILE):
                continue

            files.append(file_path)

    files.sort()

    return files


def create_baseline(directory):
    """
    Scan the directory and create a baseline.
    """

    baseline = {}

    print("\n[+] Creating baseline...\n")

    files = get_files(directory)

    for file_path in files:

        file_hash = calculate_hash(file_path)

        if file_hash is not None:

            relative_path = os.path.relpath(
                file_path,
                directory
            )

            baseline[relative_path] = file_hash

    try:

        # Create data folder if it doesn't exist
        os.makedirs(DATA_FOLDER, exist_ok=True)

        with open(BASELINE_FILE, "w") as file:

            json.dump(
                baseline,
                file,
                indent=4
            )

        print("[+] Baseline created successfully.")
        print(f"[+] Files recorded: {len(baseline)}")
        print(f"[+] Baseline saved to: {BASELINE_FILE}")

    except OSError as error:

        print(f"[!] Could not save baseline: {error}")


def load_baseline():
    """
    Load the saved baseline from JSON.
    """

    if not os.path.exists(BASELINE_FILE):
        return None

    try:

        with open(BASELINE_FILE, "r") as file:

            return json.load(file)

    except (OSError, json.JSONDecodeError) as error:

        print(f"[!] Could not load baseline: {error}")

        return None


def check_integrity(directory):
    """
    Compare the current directory with the baseline.
    """

    baseline = load_baseline()

    if baseline is None:

        print("\n[!] No baseline found.")
        print("[!] Create a baseline first.\n")

        return

    print("\n[+] Integrity Check Started\n")

    current_files = {}
    unreadable_files = []

    files = get_files(directory)

    # Calculate hashes of current files
    for file_path in files:

        file_hash = calculate_hash(file_path)

        relative_path = os.path.relpath(
            file_path,
            directory
        )

        if file_hash is not None:

            current_files[relative_path] = file_hash

        else:

            unreadable_files.append(relative_path)

    new_files = []
    modified_files = []
    unchanged_files = []

    # Compare current files with baseline
    for file_path, current_hash in current_files.items():

        # File did not exist in the baseline
        if file_path not in baseline:

            new_files.append(file_path)

        # File exists but hash is different
        elif baseline[file_path] != current_hash:

            modified_files.append(file_path)

        # File exists and hash is the same
        else:

            unchanged_files.append(file_path)

    # Find deleted files
    deleted_files = []

    for file_path in baseline:

        if file_path not in current_files:

            deleted_files.append(file_path)

    # Display new files
    print("New Files:")

    if new_files:

        for file_path in new_files:

            print(f"    {file_path}")

    else:

        print("    None")

    # Display modified files
    print("\nModified Files:")

    if modified_files:

        for file_path in modified_files:

            print(f"    {file_path}")

    else:

        print("    None")

    # Display deleted files
    print("\nDeleted Files:")

    if deleted_files:

        for file_path in deleted_files:

            print(f"    {file_path}")

    else:

        print("    None")

    # Display unchanged count
    print(f"\nUnchanged Files: {len(unchanged_files)}")

    # Display unreadable files
    if unreadable_files:

        print("\nUnreadable Files:")

        for file_path in unreadable_files:

            print(f"    {file_path}")

    # Count security-relevant changes
    changes = (
        len(new_files)
        + len(modified_files)
        + len(deleted_files)
    )

    print()

    if changes > 0:

        print(
            f"[!] {changes} security-relevant changes detected."
        )

    else:

        print("[+] No changes detected.")

    if unreadable_files:

        print(
            f"[!] Warning: {len(unreadable_files)} "
            "file(s) could not be checked."
        )


def view_baseline():
    """
    Display the saved baseline.
    """

    baseline = load_baseline()

    if baseline is None:

        print("\n[!] No baseline found.")

        return

    print("\n========== BASELINE ==========")

    for file_path, file_hash in baseline.items():

        print(file_path)
        print(f"    SHA-256: {file_hash}")

    print("==============================\n")


def get_directory():
    """
    Ask the user for a valid directory.
    """

    directory = input(
        "Enter directory to monitor: "
    ).strip()

    if not os.path.isdir(directory):

        print("[!] Invalid directory.")

        return None

    return os.path.abspath(directory)


def show_menu():
    """
    Display the FileGuard menu.
    """

    print("\n========== FileGuard ==========")
    print("1. Create Baseline")
    print("2. Check Integrity")
    print("3. View Baseline")
    print("4. Exit")
    print("===============================")


def main():
    """
    Start the FileGuard application.
    """

    while True:

        show_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            directory = get_directory()

            if directory:

                create_baseline(directory)

        elif choice == "2":

            directory = get_directory()

            if directory:

                check_integrity(directory)

        elif choice == "3":

            view_baseline()

        elif choice == "4":

            print("\n[+] Exiting FileGuard.")

            break

        else:

            print(
                "[!] Invalid choice. "
                "Please enter 1-4."
            )


if __name__ == "__main__":
    main()
    