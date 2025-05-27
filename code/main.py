from non_planar_slicing_deformation.configuration.Configuration import Configuration
from non_planar_slicing_deformation.deformer.SimpleDeformer import SimpleDeformer
from non_planar_slicing_deformation.ui.MainApp import MainApp


def main() -> None:
    """
    Start basic components that cannot be started in other parts
    """
    configuration = Configuration(deformer=lambda: SimpleDeformer())
    MainApp(configuration).run()


if __name__ == '__main__':
    main()