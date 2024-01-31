import re
import ast
from utils import DataPreprocessing
from autocubing.main import AutoCubing,create_condition_callable
from utils import WindowCapture, Cube_image_reco

cube_type = "red"
desired_stats = [{'ATT': 33},{'Boss Damage':30,'ATT': 20}]


condition = create_condition_callable(desired_stats,cube_type)
autocubing = AutoCubing(None,condition)


autocubing.main()







