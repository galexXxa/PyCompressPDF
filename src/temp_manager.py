import os
import uuid
import shutil


class TempManager:


    def __init__(
        self,
        base_folder="temp"
    ):

        self.base_folder = base_folder

        self.session_folder = None



    def __enter__(self):

        self.session_folder = os.path.join(

            self.base_folder,

            str(uuid.uuid4())

        )


        os.makedirs(

            self.session_folder,

            exist_ok=True

        )


        return self



    def file(
        self,
        filename
    ):

        return os.path.join(

            self.session_folder,

            filename

        )



    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):


        if self.session_folder and os.path.exists(
            self.session_folder
        ):

            shutil.rmtree(
                self.session_folder
            )