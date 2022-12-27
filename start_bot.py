import asyncio

from PyQt5.QtCore import QThread, pyqtSignal
from aiogram import Bot, Dispatcher
from aiogram.utils.exceptions import ValidationError


class startBot(QThread):
    show = pyqtSignal()

    def __init__(self, mainwindow, parent=None):
        super().__init__()
        self.mainwindow = mainwindow

    def run(self):
        ui = self.mainwindow
        token = ui.token.text()
        download_folder = ui.folder.text()

        try:
            aiobot = Bot(token=token)
            bot = Dispatcher(aiobot)
        except ValidationError:
            return self.show.emit()


        @bot.message_handler(content_types=['photo', 'document', 'animation', 'video'])
        async def download_from(message):
            if message.photo:
                file_id = message.photo[-1].file_id
                file_name = f'picture_{message.photo[-1].file_unique_id}_{message.date.strftime("%Y%m%d_%H%M%S")}.jpg'
                file_type = 'Picture'
            elif message.document:
                file_id = message.document.file_id
                file_name = message.document.file_name
                file_type = 'File'
            elif message.animation:
                file_id = message.animation.file_id
                file_name = message.animation.file_name
                file_type = 'Animation'
            elif message.video:
                file_id = message.video.file_id
                file_name = message.video.file_name
                file_type = 'Video'
            await aiobot.download_file_by_id(file_id, f'{download_folder}/{file_name}')
            ui.tray_icon.showMessage("User Info:", f"{file_type} {file_name} saved to {download_folder}")
            del file_id, file_name, file_type

        if not download_folder:
            return self.show.emit()
        
        try:
            ui.start.setText("Stop")
            ui.open.setEnabled(False)
            ui.token.setEnabled(False)
            ui.tray_icon.showMessage("User Info:", "Savedgram was minimized to Tray")
            asyncio.run(bot.start_polling())
        except:
            ui.start.setText("Start")
            self.show.emit()
