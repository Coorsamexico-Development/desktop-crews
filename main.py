
from scr.config.enviroment import Enviroments
from scr.features.screws.screens.screws_screen import ScrewsScreen

if __name__ == "__main__":
    Enviroments.init_environment()
    app = ScrewsScreen()
    app.mainloop()