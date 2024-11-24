import subprocess
import os
import argparse


def main(deploy: bool = False):

    # Run the build script with platformio
    subprocess.run("pio run", shell=True, check=True)
    # If deploy is True, run the upload script
    if deploy:
        subprocess.run(
            "pio run --target upload", shell=True, check=True
        )


if __name__ == "__main__":
    # Argument parser to handle deploy option
    parser = argparse.ArgumentParser(
        description="Build and optionally deploy the project."
    )
    parser.add_argument(
        "--deploy",
        action="store_true",
        help="Deploy the project to the connected device",
    )
    args = parser.parse_args()

    main(args.deploy)

# if monitoring is ever needed run pio device monitor