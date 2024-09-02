import os
import shutil
import re

# Define input and output folders, and the name of the header file
FROM_FOLDER = 'input'
TO_FOLDER = 'output'
DEFINE_FILE = 'define.h'

# Supported audio file formats
SUPPORTED_FORMATS = ['.mp3', '.wav', '.wma']

# Macro definition name for the header file
MACRO_NAME = 'DFPLAYER_AUDIO_FILES'

# Flag to enable or disable custom sorting
ENABLE_CUSTOM_SORT = False
# Logic for splitting file names into words
WORD_SPLIT_LOGIC = ''
# Primary and secondary sorting orders for custom sorting
PRIMARY_SORT_ORDER = []
SECONDARY_SORT_ORDER = []

# Set default macro name if it is empty
if not MACRO_NAME.strip():
    MACRO_NAME = 'DFPLAYER_AUDIO_FILES'
    
# Validate the macro name against the allowed format
if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', MACRO_NAME):
    print('Invalid macro name. Please check and correct the macro name.')
    exit(1)

# Initialize the output folder and header file
if os.path.exists(DEFINE_FILE):
    os.remove(DEFINE_FILE)

if os.path.exists(TO_FOLDER):
    shutil.rmtree(TO_FOLDER)

os.makedirs(TO_FOLDER)

# Retrieve all audio files from the input folder
audio_files = [f for f in os.listdir(FROM_FOLDER) if os.path.splitext(f)[1].lower() in SUPPORTED_FORMATS]

# Check for invalid file names
invalid_names = []
for f in audio_files:
    base_name = os.path.splitext(f)[0]
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', base_name):
        invalid_names.append(base_name)

# If there are invalid file names, print an error message and exit
if invalid_names:
    print("The following macro names are invalid. Please check and correct the file names:")
    for name in invalid_names:
        print(f"Invalid name: {name}")
    exit(1)

# Custom sorting logic
if ENABLE_CUSTOM_SORT:
    split_words = []
    for base in [os.path.splitext(f)[0] for f in audio_files]:
        if WORD_SPLIT_LOGIC == 'UNDERSCORE':
            split_words.append([word.upper() for word in base.split('_')])
        elif WORD_SPLIT_LOGIC == 'CAMEL_CASE':
            split_words.append([word.upper() for word in re.findall(r'[a-z]+|[A-Z][a-z]*', base)])
        elif WORD_SPLIT_LOGIC == 'PASCAL_CASE':
            split_words.append([word.upper() for word in re.findall(r'[A-Z][a-z]*', base)])
        else:
            print('Invalid word split logic.')
            exit(1)

    # Convert primary and secondary sorting orders to uppercase
    PRIMARY_SORT_ORDER = [tag.upper() for tag in PRIMARY_SORT_ORDER]
    SECONDARY_SORT_ORDER = [tag.upper() for tag in SECONDARY_SORT_ORDER]

    # Calculate priority for each file based on the sorting logic
    file_priorities = []
    for index, parts in enumerate(split_words):
        if len(parts) < 2:
            priority = float('inf')  # Set priority to infinity for files with fewer than two parts
        else:
            primary_tag = parts[0]
            secondary_tag = parts[1] if len(parts) > 1 else ''

            primary_priority = PRIMARY_SORT_ORDER.index(primary_tag) if primary_tag in PRIMARY_SORT_ORDER else len(PRIMARY_SORT_ORDER)
            secondary_priority = SECONDARY_SORT_ORDER.index(secondary_tag) if secondary_tag in SECONDARY_SORT_ORDER else len(SECONDARY_SORT_ORDER)

            priority = primary_priority * 100 + secondary_priority

        file_priorities.append((priority, audio_files[index]))

    # Sort files based on their priority
    file_priorities.sort()

else:
    # If custom sorting is not enabled, keep files in their original order
    file_priorities = [(i, audio_files[i]) for i in range(len(audio_files))]

# Create the header file and copy the files to the output folder
with open(DEFINE_FILE, 'w') as define_file:
    define_file.write(f"#ifndef {MACRO_NAME}\n#define {MACRO_NAME}\n\n")

    for index, (priority, audio_file) in enumerate(file_priorities):
        new_filename = f"{index + 1:04}{os.path.splitext(audio_file)[1]}"
        shutil.copy(os.path.join(FROM_FOLDER, audio_file), os.path.join(TO_FOLDER, new_filename))
        base_name = os.path.splitext(audio_file)[0]
        define_file.write(f"#define {base_name} {index + 1}\n")
        print(f"File name: {base_name}, corresponding number: {index + 1:04}")

    define_file.write("\n#endif\n")

print("Files copied and define.h generated successfully.")
