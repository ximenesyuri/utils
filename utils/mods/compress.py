import os
import tarfile
import zipfile
from utils.mods.cmd import cmd
from utils.mods.path import path
from utils.err import CompressErr

class compress:
    def compress(input_path, output_path):
        if path.extension(output_path) == '.tar.gz':
            compress.tar.compress(input_path, output_path)
        elif path.extension(output_path) == 'zip':
            compress.zip.compress(input_path, output_path)
        else:
            raise CompressErr(f"Unsupported compression type: '{path.extension(output_path)}'")

    def extract(input_path, output_dir):
        if path.extension(input_path) == '.tar.gz':
            compress.tar.extract(input_path, output_dir)
        elif path.extension(input_path) == 'zip':
            compress.zip.extract(input_path, output_dir)
        else:
            raise CompressErr(f"Unsupported compression type: '{path.extension(input_path)}'")

    class tar:
        def compress(input_path, output_path):
            with tarfile.open(output_path, "w:gz") as tar:
                if os.path.isdir(input_path):
                    for root, dirs, files in os.walk(input_path):
                        for file in files:
                            filepath = os.path.join(root, file)
                            arcname = os.path.relpath(filepath, input_path)
                            tar.add(filepath, arcname=arcname)
                        for dir in dirs:
                            dirpath = os.path.join(root, dir)
                            arcname = os.path.relpath(dirpath, input_path)
                            tar.add(dirpath, arcname=arcname)
                elif os.path.isfile(input_path):
                     tar.add(input_path, arcname=os.path.basename(input_path))
                else:
                    raise CompressErr(f"Input path not found or not a file/directory: {input_path}")

        def extract(input_path, output_dir):
            with tarfile.open(input_path, 'r:gz') as tar:
                tar.extractall(path=output_dir)

    class zip:
        def compress(input_path, output_path):
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.isdir(input_path):
                    for root, dirs, files in os.walk(input_path):
                        for file in files:
                            filepath = os.path.join(root, file)
                            arcname = os.path.relpath(filepath, start=input_path)
                            zipf.write(filepath, arcname=arcname)
                        for dir in dirs:
                             dirpath = os.path.join(root, dir)
                             arcname = os.path.relpath(dirpath, start=input_path)
                             zipf.write(dirpath, arcname + os.sep)

                elif os.path.isfile(input_path):
                    zipf.write(input_path, arcname=os.path.basename(input_path))
                else:
                     raise CompressErr(f"Input path not found or not a file/directory: {input_path}")

        def extract(input_path, output_dir):
            with zipfile.ZipFile(input_path, 'r') as zipf:
                zipf.extractall(path=output_dir)
