import argparse

from non_planar_slicing_deformation.common.MainLogger import MAIN_LOGGER
from non_planar_slicing_deformation.configuration.CurrentDeformerState import CurrentDeformerState
from non_planar_slicing_deformation.configuration.Configuration import Configuration
from non_planar_slicing_deformation.deformer.SimpleDeformer import SimpleDeformer
from non_planar_slicing_deformation.ui.MainApp import MainApp
from non_planar_slicing_deformation.state.DeformerState import DeformerState
from non_planar_slicing_deformation.undeformer.SimpleUndeformer import SimpleUndeformer


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

    configuration = Configuration(deformer=lambda: SimpleDeformer(), undeformer=lambda: SimpleUndeformer(),
                                  stateType=DeformerState)
    CurrentDeformerState(configuration.stateType)
    MainApp(configuration).run()


if __name__ == '__main__':
    main()
