from pathlib import Path
import core


def get_resource_path(parts):
    return Path(core.__file__).parent.joinpath(*parts)