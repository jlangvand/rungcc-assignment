# Browser compiler frontent

## Features
Lets you compile and run code (as for now only C++ using CMake) from your browser.

## Usage
Simply run `pip install .`, then `python -m rungcc`. Server runs on 127.0.0.1:8080 by default.

## Limitations
Do *not* run this on a public server. Although the compiled code runs in a sandbox, the server lacks any kind of safeguards or limitations on resource usage, etc.

It's probably very bug-ridden, especially related to character encoding.

Have fun.
