import os
import tarfile
from utils.mods.cmd import cmd
from utils.err import CompressErr

class compress:
    class tar:
        def compress(input_path, output_path):
            output_dir = os.path.dirname(output_path)
            cmd.mkd(output_dir)
            try:
                with tarfile.open(output_path, "w:gz") as tar:
                    for root, dirs, files in os.walk(input_path):
                        for file in files:
                            filepath = os.path.join(root, file)
                            tar.add(filepath, arcname=os.path.relpath(filepath, input_path))
                        for dir in dirs:
                            dirpath = os.path.join(root, dir)
                            tar.add(dirpath, arcname=os.path.relpath(dirpath, input_path))
            except Exception as e:
                raise CompressErr(e)

        def extract(input_path, output_dir):
            try:
                with tarfile.open(input_path, 'r:gz') as tar:
                    tar.extractall(path=output_dir)
            except Exception as e:
                raise CompressErr(e)
