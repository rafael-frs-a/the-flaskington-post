from logging import FileHandler, WARNING

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)


def init_app(app):
    app.logger.addHandler(file_handler)
