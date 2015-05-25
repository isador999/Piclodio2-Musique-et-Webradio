import alsaaudio


class AudioManager():
    def __init__(self):
        if 'Master' in self._get_available_card():
            self.master = alsaaudio.Mixer(control='Master')
        else:
            self.master = None
        self.pcm = alsaaudio.Mixer(control='PCM')

    def togglemute(self):
        if 0 in self.pcm.getmute():
            self.pcm.setmute(1)
            if self.master is not None:
                self.master.setmute(1)
        else:
            self.pcm.setmute(0)
            if self.master is not None:
                self.master.setmute(0)

    def volume_up(self):
        try:
            current_volume = self.get_percent_volume()
            print current_volume
            self.pcm.setvolume(int(current_volume)+5)
        except alsaaudio.ALSAAudioError:
            self.pcm.setvolume(100)

    def volume_down(self):
        try:
            current_volume = self.get_percent_volume()
            self.pcm.setvolume(int(current_volume)-5)
        except alsaaudio.ALSAAudioError:
            self.pcm.setvolume(0)

    def set_volume(self, value):
        self.pcm.setvolume(value)

    def get_percent_volume(self):
        return int(self.pcm.getvolume()[0])

    def _get_available_card(self):
        return alsaaudio.mixers()

    def get_mute_status(self):
        current_mute = self.pcm.getmute()
        if 0 in current_mute:
            return "on"
        else:
            return "off"







