"""Base module with common functions"""


class ToolframeModule:
    @staticmethod
    def _get_input():
        import fileinput
        for line in fileinput.input():
            yield line.strip()

    @staticmethod
    def _save_to_file(filename: str, lines):
        with open(filename, 'w') as file:
            file.writelines(lines)

    @staticmethod
    def _append_to_file(filename: str, line: str):
        with open(filename, 'a') as file:
            file.write('{}\n'.format(line))
