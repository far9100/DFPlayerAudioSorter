# README

## Overview

This script is designed to organize audio files into a format suitable for use with the [DFPlayer Mini MP3](https://wiki.dfrobot.com/DFPlayer_Mini_SKU_DFR0299) player module. It allows you to sort audio files based on user-defined logic, rename them to sequential numbers, and generate a header file ("define.h"). This header file maps the original filenames to new numeric identifiers, enabling you to reference audio files by name rather than by number in your program.

## Features

- **Custom Sorting**:
  
  Allows you to sort files based on specific word-splitting logic or predefined sorting orders.

- **Automatic Macro Name Validation**:
  
  Ensures that the macro names derived from file names adhere to valid naming conventions. The script automatically checks and reports any invalid macro names, which might include characters that are not allowed in macro definitions. This helps in avoiding issues related to invalid macro names in your header file.

- **File Renaming and Header File Generation**:
  
  Automatically renames files to sequential numbers and generates a `define.h` file. This header file provides macro definitions that map each original filename to its corresponding numeric identifier, allowing you to reference audio files by name in your code instead of by numeric identifiers.

## Prerequisites

- Python 3.x
- Required Python libraries: `os`, `shutil`, `re`

## Configuration

The script includes several configurable variables:

- `FROM_FOLDER`: The folder containing the original audio files.
- `TO_FOLDER`: The folder where the sorted and renamed files will be saved.
- `DEFINE_FILE`: The name of the header file to be generated.
- `SUPPORTED_FORMATS`: List of supported audio file formats.
- `MACRO_NAME`: The macro name used in the generated header file. If not provided, the default value `DFPLAYER_AUDIO_FILES` will be used.
- `ENABLE_CUSTOM_SORT`: When set to `True`, enables custom sorting logic based on `WORD_SPLIT_LOGIC` and `PRIMARY_SORT_ORDER`. When set to `False`, files are processed in their original order.
- `WORD_SPLIT_LOGIC`: Defines how filenames are split for sorting. Possible values include:
  - `'UNDERSCORE'`: Splits filenames by underscores (`_`) into different parts.
  - `'CAMEL_CASE'`: Splits filenames based on camel case naming, e.g., `fileName` will be split into `file` and `Name`.
  - `'PASCAL_CASE'`: Splits filenames based on Pascal case naming, e.g., `FileName` will be split into `File` and `Name`.
- `PRIMARY_SORT_ORDER`: List of primary sorting tags. These tags are used to determine sorting priority. If parts of the filename match tags in this list, they will be sorted according to these tags.
- `SECONDARY_SORT_ORDER`: List of secondary sorting tags. When primary sorting tags are the same, secondary sorting tags determine the order between files.

## Usage

1. **Set Up Folders**:
   
   Place audio files in the `FROM_FOLDER` and adjust the configuration variables in the script as needed.

2. **Run the Script**:
   
   Execute the script using Python 3:
   ```bash
   python DFPlayerAudioSorter.py
   ```
   The sorted and renamed audio files will be saved in the `TO_FOLDER`. Additionally, the `define.h` file will be generated in the script directory, containing macro definitions that map each original filename to its corresponding numeric identifier.

## Examples

Here are examples of different configurations to help you understand how the script works:

- ### Default Order ###

    **Configuration**:
    ```py
    ENABLE_CUSTOM_SORT = False
    ```

    In this configuration, `ENABLE_CUSTOM_SORT` is set to `False`, meaning the script will not use any custom sorting logic and will process files in their original order.

    **Input Folder**:
    ```
    input/
    ├── example1.mp3
    ├── example2.mp3
    └── example3.mp3
    ```

    The `input` folder contains three audio files named `example1.mp3`, `example2.mp3`, and `example3.mp3`, ordered by filename.

    **Output Folder**:
    ```
    output/
    ├── 0001.mp3
    ├── 0002.mp3
    └── 0003.mp3
    ```

    In the `output` folder, files are renamed to sequential numbers in a four-digit format with the `.mp3` extension, maintaining the original order.

    **`define.h` File**:
    ```c++
    #ifndef DFPLAYER_AUDIO_FILES
    #define DFPLAYER_AUDIO_FILES

    #define example1 1
    #define example2 2
    #define example3 3

    #endif
    ```

    The generated `define.h` file maps each original filename to its corresponding numeric identifier. These macro definitions allow you to reference audio files by names like `example1` instead of numeric identifiers like `1`.

- ### Using `UNDERSCORE` Custom Sorting ###

    **Configuration**:
    ```py
    ENABLE_CUSTOM_SORT = True
    WORD_SPLIT_LOGIC = 'UNDERSCORE'
    PRIMARY_SORT_ORDER = ['MUSIC', 'SOUND']
    SECONDARY_SORT_ORDER = ['INTRO', 'OUTRO']
    ```

    In this configuration, `ENABLE_CUSTOM_SORT` is set to `True`, enabling custom sorting. `WORD_SPLIT_LOGIC` is set to `'UNDERSCORE'`, meaning filenames will be split by underscores (`_`). `PRIMARY_SORT_ORDER` and `SECONDARY_SORT_ORDER` define the primary and secondary sorting tags.

    **Input Folder**:
    ```
    input/
    ├── music_intro.mp3
    ├── music_outro.mp3
    └── sound_effect.mp3
    ```

    The `input` folder contains filenames with underscores (`_`) separating different parts. The script will sort files based on these parts.

    **Output Folder**:
    ```
    output/
    ├── 0001.mp3  # music_intro.mp3
    ├── 0002.mp3  # music_outro.mp3
    └── 0003.mp3  # sound_effect.mp3
    ```

    In the `output` folder, files are renamed according to custom sorting logic. `music_intro.mp3` is first, as it matches the primary sorting tag `MUSIC` and secondary tag `INTRO`. It is followed by `music_outro.mp3` and `sound_effect.mp3`.

    **`define.h` File**:
    ```c++
    #ifndef DFPLAYER_AUDIO_FILES
    #define DFPLAYER_AUDIO_FILES

    #define music_intro 1
    #define music_outro 2
    #define sound_effect 3

    #endif
    ```

    The generated `define.h` file maps each filename to its corresponding numeric identifier, adjusted according to custom sorting logic.

- ### Using `CAMEL_CASE` Custom Sorting ###

    **Configuration**:
    ```py
    ENABLE_CUSTOM_SORT = True
    WORD_SPLIT_LOGIC = 'CAMEL_CASE'
    PRIMARY_SORT_ORDER = ['INTRO', 'EFFECT']
    SECONDARY_SORT_ORDER = []
    ```

    In this configuration, `ENABLE_CUSTOM_SORT` is set to `True`, enabling custom sorting. `WORD_SPLIT_LOGIC` is set to `'CAMEL_CASE'`, meaning filenames will be split according to camel case naming. `PRIMARY_SORT_ORDER` defines the primary sorting tags, with no secondary tags specified.

    **Input Folder**:
    ```
    input/
    ├── introMusic.mp3
    ├── outroMusic.mp3
    └── soundEffect.mp3
    ```

    The `input` folder contains filenames following camel case naming.

    **Output Folder**:
    ```
    output/
    ├── 0001.mp3  # introMusic.mp3
    ├── 0002.mp3  # outroMusic.mp3
    └── 0003.mp3  # soundEffect.mp3
    ```

    In the `output` folder, files are renamed according to custom sorting logic. `introMusic.mp3` is first, as it matches the primary sorting tag `INTRO`. It is followed by `outroMusic.mp3` and `soundEffect.mp3`, ordered based on custom sorting logic.

    **`define.h` File**:
    ```c++
    #ifndef DFPLAYER_AUDIO_FILES
    #define DFPLAYER_AUDIO_FILES

    #define introMusic 1
    #define outroMusic 2
    #define soundEffect 3

    #endif
    ```

    The generated `define.h` file maps each filename to its corresponding numeric identifier, adjusted according to custom sorting logic.

## Error Descriptions

- **Invalid Macro Name**:
  
  If the `MACRO_NAME` contains invalid characters or is empty, the script will terminate with the message: 
  ```
  Invalid macro name. Please check and correct the macro name.
  ```

- **Invalid Filename for Macro Definitions**:
  
  If any of the audio file names contain invalid characters for macro definitions (e.g., spaces, special characters), the script will terminate with the message:
  ```
  The following macro names are invalid. Please check and correct the file names:
  Invalid Name: <filename>
  ```

- **Invalid Word Split Logic**:
  
  If an unsupported `WORD_SPLIT_LOGIC` value is specified, the script will terminate with the message:
  ```
  Invalid word split logic.
  ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.