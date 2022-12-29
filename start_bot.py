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

        @bot.message_handler(content_types=['animation', 'audio', 'document', 'photo', 'video', 'voice'])
        async def download_from(message):
        
            file = {}
            
            if message.animation:
                atr = ('media', 'mp4')
                file.update(message.animation)
            elif message.audio:
                atr = ('audio', 'mp3')
                file.update(message.audio)
            elif message.document:
                atr = ('document', 'file')
                file.update(message.document)
            elif message.photo:
                atr = ('picture', 'jpg')
                file.update(message.photo[-1])
            elif message.video:
                atr = ('video', 'mp4')
                file.update(message.video)
            elif message.voice:
                atr = ('audio', 'ogg')
                file.update(message.voice)
            
            if file['file_size'] > 20971520:
                ui.tray_icon.showMessage("User Info:", f"{atr[0].capitalize()} {file['file_name']} size too big! Can't download")
            else:
                if not file.get('file_name'):
                    file['file_name'] = f"{atr[0]}_{file['file_unique_id']}_{message.date.strftime('%Y%m%d_%H%M%S')}.{atr[1]}"
                ui.tray_icon.showMessage("User Info:", f"{atr[0].capitalize()} {file['file_name']} download started")
                await aiobot.download_file_by_id(file['file_id'], f"{download_folder}/{file['file_name']}")
                ui.tray_icon.showMessage("User Info:", f"{atr[0].capitalize()} {file['file_name']} saved to {download_folder}")
            
            del atr, file

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
