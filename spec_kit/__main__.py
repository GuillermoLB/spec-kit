"""Allow spec-kit to be run as a module: python -m spec_kit"""

import sys
from spec_kit.cli import main

if __name__ == '__main__':
    sys.exit(main())
