import argparse

from non_planar_slicing_deformation.common.MainLogger import MAIN_LOGGER
from non_planar_slicing_deformation.configuration.CurrentDeformerState import CurrentDeformerState
from non_planar_slicing_deformation.ui.MainApp import MainApp


def main() -> None:
    """
    Start basic components that cannot be started in other parts
    """
    parser = argparse.ArgumentParser(
        prog="NonPlanarSlicingDeformation", description="A deformation tool for non planar slicing"
    )
    parser.add_argument('--test', action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.test:
        # This means that the executable was run in test mode to check that it was correctly created
        MAIN_LOGGER.info("Executable runs")
        return

    MainApp().run()


if __name__ == '__main__':
    main()
