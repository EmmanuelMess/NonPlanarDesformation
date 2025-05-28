from configuration.CurrentDeformerState import CurrentDeformerState
from non_planar_slicing_deformation.configuration.Configuration import Configuration
from non_planar_slicing_deformation.deformer.SimpleDeformer import SimpleDeformer
from non_planar_slicing_deformation.ui.MainApp import MainApp
from state.DeformerState import DeformerState
from undeformer.SimpleUndeformer import SimpleUndeformer


def main() -> None:
    """
    Start basic components that cannot be started in other parts
    """
    configuration = Configuration(deformer=lambda: SimpleDeformer(), undeformer=lambda: SimpleUndeformer(),
                                  stateType=DeformerState)
    CurrentDeformerState(configuration.stateType)
    MainApp(configuration).run()


if __name__ == '__main__':
    main()