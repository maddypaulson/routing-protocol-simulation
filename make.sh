#!/bin/bash

# Check if Python is installed
if command -v python &> /dev/null; then
    python_cmd="python"
elif command -v python3 &> /dev/null; then
    python_cmd="python3"
else
    echo "Python is not installed. Please install Python."
    exit 1
fi

# Upgrade pip
pip install --upgrade pip

# Install required Python packages
echo "Installing required Python packages..."
pip install  pyinstaller

# Check if installations were successful
if [ $? -ne 0 ]; then
    echo "Failed to install required Python packages. Please check your Python environment."
    exit 1
fi

# Define source files
source_files=("dvr" "lsr")

# Create binary executables
echo "Creating binary executables..."
for file in "${source_files[@]}"; do
    src_file="src/${file}.py"
    if [ -f "$src_file" ]; then
        echo "Creating binary executable for $src_file..."
        pyinstaller --onefile "$src_file"
    else
        echo "Source file $src_file not found."
        exit 1
    fi
done

echo "Binary executables created successfully."



# Remove the build folder
echo "Removing the build folder..."
rm -rf build

# Remove the .spec files
echo "Removing .spec files..."
for file in "${source_files[@]}"; do
    rm -rf "${file}.spec"
    echo "Removed ${file}.spec"
done

