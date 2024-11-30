from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:
    """
    Reads the requirements file and returns a list of dependencies.

    Args:
        file_path (str): Path to the requirements file.

    Returns:
        List[str]: A list of dependencies from the requirements file.
    """
    try:
        with open(file_path, "r") as f:
            requirements = f.readlines()
            # Remove newline characters and clean up the list
            requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("#")]
            # Remove editable install flag if present
            if HYPHEN_E_DOT in requirements:
                requirements.remove(HYPHEN_E_DOT)
        return requirements
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The requirements file '{file_path}' does not exist.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the requirements file: {e}")

# Test the function (optional for debugging)
if __name__ == "__main__":
    print(get_requirements("./requirements.txt"))
