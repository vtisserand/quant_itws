#!/bin/bash

# Define your main LaTeX document filename (without the .tex extension)
main_file="main"

# Create the "output" folder if it doesn't exist
mkdir -p output

# Run pdflatex to compile the document
pdflatex -output-directory=output -interaction=nonstopmode "$main_file.tex"

# Move the resulting PDF to the current working directory (cwd)
mv "output/$main_file.pdf" .

# Clean up auxiliary files (optional)
# Uncomment the following lines if you want to remove the auxiliary files
# rm "output/$main_file.aux" "output/$main_file.log" "output/$main_file.out"

# Display a message to indicate completion
echo "Compilation complete. The PDF is in the current working directory."
