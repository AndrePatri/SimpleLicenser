### SimpleLicenser

First, add a licence to your project following the instructions [here](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository).

After having done that, it is good practice to also add a header to each code file in you project, so that from individual code is always possible to go back to the original licence. 
This "package" holds a simple but effective script to automate this otherwise tedious procedure.

Usage example: `python simplelicenser/simple_licenser.py --license_key=GPLv2 --project_name={YourProject} --authors="John Doe and Jane Doe" --root_path=/{path_to_your_files} --extensions .js .py .cpp`

Headers are automatically added with the right comment characters for most used programming languages. Feel free to add missing ones by creating a pull request.

Preexisting licences are checked using either a default keyword or the full licences. By default, the search is based on the keyword approach, but you can enable exact search with the argument `--check_exact`.

Optionally, you can exclude given patterns from the licence with `--exclude_patterns pattern1 pattern2 ... patternN`.

Supported licenses: 
- MIT License: One of the most open and permissive licenses. Allows for almost unrestricted freedom as long as the original license and copyright notice are included with any substantial portions of the software.
- GNU General Public License (GPL): Requires that modified versions of the project also be open-source and distributed under the GPL license.

    - GPLv2: The second version of the GNU GPL.
    - GPLv3: Introduces additional permissions and protections from tivoization.
- Apache 2.0: Similar to the MIT License with additional clauses concerning patent rights.
- BSD: There are mainly two types of BSD licenses:

    - BSD 2-Clause License: Very permissive, similar to the MIT license.
    - BSD 3-Clause License: Adds a clause against using the name of the project or its contributors without permission.
- GNU Lesser General Public License (LGPL): Similar to GPL, but allows linking to proprietary modules. It comes in two main versions:

    - LGPLv2.1
    - LGPLv3
- GNU Affero General Public License (AGPL): Similar to the GPL but also requires that the source code be made available to any network user of the licensed work, typically a web application.
- Mozilla Public License 2.0: Allows users to freely use, modify, and distribute the code, but they must disclose the source of their own derivative works and distribute them under the same license.

As a side note, when choosing a license, consider the following aspects:

- Your willingness to contribute to the open-source community: More permissive licenses contribute more freely to the community.
- Use of third-party code: If you're using other open-source libraries, their licenses might dictate your project's license.
- Corporate/organizational policies: Sometimes, your employer or stakeholder might have policies dictating license choice.

You can utilize tools like [ChooseALicense.com](ChooseALicense.com) to help guide you to a license that suits your intent and project needs.