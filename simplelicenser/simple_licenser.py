# Copyright (C) 2023, AndrePatri
# All rights reserved.
# 
# This file is part of SimpleLicenser and distributed under the BSD 3-Clause License.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
import os
import shutil
import argparse
from datetime import datetime
import re

# Define a mapping between file extensions and comment characters
COMMENT_CHARS = {
    '.py': ('#', ''),          # Python
    '.js': ('//', ''),         # JavaScript
    '.cpp': ('//', ''),        # C++
    '.c': ('//', ''),          # C
    '.hpp': ('//', ''),        # C++ Header
    '.h': ('//', ''),          # C Header
    '.sh': ('#', ''),          # Shell Script
    '.java': ('//', ''),       # Java
    '.rb': ('#', ''),          # Ruby
    '.cs': ('//', ''),         # C#
    '.go': ('//', ''),         # Go
    '.r': ('#', ''),           # R
    '.m': ('%', ''),           # MATLAB
    '.pl': ('#', ''),          # Perl
    '.php': ('//', ''),        # PHP
    '.ts': ('//', ''),         # TypeScript
    '.swift': ('//', ''),      # Swift
    '.kts': ('//', ''),        # Kotlin Script
    '.kt': ('//', ''),         # Kotlin
    '.f': ('c', ''),           # Fortran
    '.for': ('c', ''),         # Fortran
    '.f90': ('!', ''),         # Fortran 90
    '.f95': ('!', ''),         # Fortran 95
    '.lua': ('--', ''),        # Lua
    '.sql': ('--', ''),        # SQL
    '.ada': ('--', ''),        # Ada
    '.html': ('<!--', '-->'),  # HTML
    '.xml': ('<!--', '-->'),   # XML
    '.rhtml': ('<%#', '%>'),   # RHTML
    '.css': ('/*', '*/'),      # CSS
    '.scss': ('//', ''),       # SCSS
    '.yml': ('#', ''),         # YAML
    '.yaml': ('#', ''),        # YAML
    '.json': ('//', ''),       # JSON (Note: JSON standard does not support comments, but some parsers do)
    '.ini': (';', ''),         # INI
    '.tex': ('%', ''),         # LaTeX
    '.matlab': ('%', ''),      # MATLAB
    '.vbs': ("'", ''),         # Visual Basic Script
    '.vb': ("'", ''),          # Visual Basic
    '.bas': ("'", ''),         # Basic
    '.ps1': ('#', ''),         # PowerShell
    # Add other extensions and comment characters as needed
}

# Keyword to recognize licenses
LICENSE_KEYWORD = "Copyright (C)"

# Keyword to recognize licenses
LICENSE_EXCLUDEPATHS = ["__init__" # python packages
                    ]

# Supported license headers
LICENSE_HEADERS = {
    "GPLv2": """ {year}  {authors}

This file is part of {project_name} and distributed under the General Public License version 2 license.

{project_name} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

{project_name} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with {project_name}.  If not, see <http://www.gnu.org/licenses/>.
""",

    "MIT": """ {year} {authors}

This file is part of {project_name} and distributed under the MIT License.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",

    "Apache 2.0": """ {year} {authors}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
""",
    
    "BSD-3": """ {year}, {authors}
All rights reserved.

This file is part of {project_name} and distributed under the BSD 3-Clause License.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
""",

    "BSD-2": """ {year}, {authors}
All rights reserved.

This file is part of {project_name} and distributed under the BSD 2-Clause License.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
""",
    
    "LGPLv2.1": """ {year} {authors}

This file is part of {project_name} and distributed under the GNU Lesser General Public License v2.1.

{project_name} is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 2.1 of the License, or
(at your option) any later version.

{project_name} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with {project_name}.  If not, see <http://www.gnu.org/licenses/>.
""",
    
    "LGPLv3": """ {year} {authors}

This file is part of {project_name} and distributed under the GNU Lesser General Public License v3.

{project_name} is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

{project_name} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with {project_name}.  If not, see <http://www.gnu.org/licenses/>.
""",
    
    "GPLv3": """ {year} {authors}

This file is part of {project_name} and distributed under the GNU General Public License v3.

{project_name} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

{project_name} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with {project_name}.  If not, see <http://www.gnu.org/licenses/>.
""",

    "AGPLv3": """ {year} {authors}

This file is part of {project_name} and distributed under the GNU Affero General Public License v3.

{project_name} is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

{project_name} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with {project_name}.  If not, see <https://www.gnu.org/licenses/>.
""",
    
    "MPL-2.0": """
    This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. 
If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Copyright {year} {authors}
"""
}

def check_license_header(file_path, 
                    license_header):
    """
    Check if the license header already exists in the file.
    
    Parameters:
        file_path (str): The path to the file to check.
        license_header (str): The license header text to check for.

    Returns:
        bool: True if the header exists, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Using regular expression to handle variations in spacing and line breaks
            license_regex = re.escape(license_header).replace('\\n', '\\s*\\n\\s*')
            return re.search(license_regex, content) is not None
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def check_all_headers_exactly(file_path, 
                year, 
                authors, 
                project_name, 
                comment_char):

    keysList = list(LICENSE_HEADERS.keys())

    already_there = {}

    found_preexisting_license = False

    for licensetype in keysList:

        license_header = format_license_header(
                LICENSE_HEADERS[licensetype].format(year=year, 
                                                    authors=authors, 
                                                    project_name=project_name),
                comment_char
            )
        
        there = check_license_header(file_path, license_header)

        if there:

            already_there[licensetype] = True

            warning = "Warning: already found licence of type " + \
                f"{licensetype}" + " in " + f"{file_path} with data \n" + \
                f"authors: {authors}, project_name: {project_name}, year: {year}.\n"+ \
                "No license will be added here."
            
            print(warning)

            found_preexisting_license = True

        else:
            
            already_there[licensetype] = False

    return not found_preexisting_license

def check_headers_approx(file_path, 
                comment_char):

    keyword = f"{comment_char[0]}" + F" {LICENSE_KEYWORD}"

    there = check_license_header(file_path, keyword)

    if there:

        warning = "Warning: the file at " + \
                f"{file_path} contains a license already (most likely).\n" + \
                f"The search was based on the pattern \"{keyword}\".\n" + \
                "No header will be added for safety."
            
        print(warning)
        
    return not there

def format_license_header(license_header, 
                    comment_chars):

    comment_start, comment_end = comment_chars

    # Handling for comment styles that have closing characters.
    if comment_end.strip():

        return f"{comment_start}\n{license_header}\n{comment_end}"
    
    # Handling for comment styles that do not have closing characters.
    else:

        formatted_lines = []

        keyword_added = False

        for line in license_header.split('\n'):
            
            if keyword_added:

                formatted_lines.append(f"{comment_start} {line}")

            if not keyword_added:
                
                # adding keyword to detect licences on
                # first line

                keyword_added = True

                formatted_lines.append(f"{comment_start} {LICENSE_KEYWORD}{line}")

        return '\n'.join(formatted_lines)

def add_header(file_path, license_header, create_backup=False):
    
    if create_backup:

        shutil.copy(file_path, file_path + '.bak')

    with open(file_path, 'r+') as f:

        content = f.read()

        f.seek(0, 0)

        f.write(license_header + '\n' + content)

def main(license_key, 
        project_name, 
        authors, 
        root_path, 
        extensions, 
        create_backup=False, 
        exact_check=False, 
        exclude_paths = []):

    year = datetime.now().year

    if not os.path.exists(root_path):

        error = f"The path {root_path} does not exist."

        raise Exception(error)
    
    elif not os.path.isdir(root_path):
        
        error = f"The path {root_path} is not a directory."

        raise Exception(error)

    for root, dirs, files in os.walk(root_path):

        for file in files:

            filename, file_ext = os.path.splitext(file)  # Extract file extension

            exclude = False

            for exclude_path in exclude_paths:

                if bool(re.search(exclude_path, filename)):
                    
                    message = f"Skipping {file} since it matches exclusion pattern {exclude_path}"

                    print(message)

                    exclude = True
            
            if any(file.endswith(ext) for ext in extensions) and \
                not exclude:

                comment_char = COMMENT_CHARS.get(file_ext, 
                                                '#')  # Get comment char or default to '#'

                file_path = os.path.join(root, file)

                formatted_license_header = format_license_header(
                    LICENSE_HEADERS[license_key].format(year=year, 
                                                        authors=authors, 
                                                        project_name=project_name),
                    comment_char
                )
                
                check_ok = False
                
                if exact_check:

                    check_ok = check_all_headers_exactly(file_path, 
                                    year, 
                                    authors, 
                                    project_name, 
                                    comment_char)
                else:

                    check_ok = check_headers_approx(file_path, comment_char)

                if check_ok:

                    add_header(os.path.join(root, file), formatted_license_header, create_backup)
                    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Add a license header to all files of specified types in a directory')
    
    parser.add_argument('--license_key', required=True, choices=LICENSE_HEADERS.keys(), 
                        help='Type of license. Options: ' + ', '.join(LICENSE_HEADERS.keys()))
    parser.add_argument('--project_name', required=True, 
                        help='Name of the project')
    parser.add_argument('--authors', required=True, 
                        help='Name of the author(s) or organization')
    parser.add_argument('--root_path', required=True, 
                        help='Root path from where the search should begin')
    parser.add_argument('--extensions', nargs='+', default=['.py'], 
                        help='File extensions to apply the license to (default: .py)')
    # Add argument for backup
    parser.add_argument('--create_backup', action='store_true', 
                        help='Create a backup of files before adding license header. Default is False.')
    
    parser.add_argument('--check_exact', action='store_true',
                        help='Checks if an license with same authors, project and year was already added.')
    
    parser.add_argument('--exclude_paths', nargs='+', default=LICENSE_EXCLUDEPATHS, 
                        help='Patterns used to exlude given files.')
    
    args = parser.parse_args()

    main(args.license_key, 
        args.project_name, 
        args.authors, 
        args.root_path, 
        args.extensions, 
        args.create_backup, 
        args.check_exact, 
        args.exclude_paths)