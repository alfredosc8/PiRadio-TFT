#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classes.Config import Config
from libs.fenix.program import Program
from libs.fenix.program import Process
from classes.VolumeBar import VolumeBar
import textwrap
import datetime


class AppRadio(Process):

    main = None
    font_big = None
    font_small = None
    font_tiny = None
    title = ''
    last_title = ''
    song = ''
    last_song = ''
    last_song_fetch = 0
    blinked = False
    last_blinked = 0

    def begin(self, main):

        self.main = main
        self.x = 0
        self.y = 0
        self.font_big = Program.load_fnt(Config.menu_font_bold, Config.font_size_big)
        self.font_small = Program.load_fnt(Config.menu_font_bold, Config.font_size_small)
        self.font_tiny = Program.load_fnt(Config.menu_font, Config.font_size_small)
        self.title = self.main.fetch_station_title()
        self.song = self.main.fetch_song_title()

        # station
	x_offset = 10
        offset = 16
        label_station = Program.write(self.font_big, x_offset, offset, 0, self.title)
        label_station.colour = Config.color_white

        # song 1
        offset = offset + Config.font_size_big + 8
        label_song1 = Program.write(self.font_small, x_offset, offset, 0, '')
        label_song1.colour = Config.color_white

        # song 2
        offset = offset + Config.font_size_small + 2
        label_song2 = Program.write(self.font_small, x_offset, offset, 0, '')
        label_song2.colour = Config.color_white

        # song 3
        offset = offset + Config.font_size_small + 2
        label_song3 = Program.write(self.font_small, x_offset, offset, 0, '')
        label_song3.colour = Config.color_white

        # song 4
        offset = offset + Config.font_size_small + 2
        label_song4 = Program.write(self.font_small, x_offset, offset, 0, '')
        label_song4.colour = Config.color_white

        # channel
        offset = offset + Config.font_size_small + 12
        VolumeBar(self.main, x_offset-5, offset, 100, 100, 12, Config.color_white)
        VolumeBar(self.main, x_offset+1-5, offset+1, 100, 100, 10, Config.color_black)
        bar = VolumeBar(self.main, x_offset+2-5, offset+2, self.main.channel+1, len(self.main.playlist.playlist), 8, Config.color_white)

        offset = offset + 16
        label_pos = Program.write(self.font_small, x_offset, offset, 0, '')
        label_pos.colour = Config.color_white

        # clock
        label_clock = Program.write(self.font_small, self.main.screen_size[0] - 5*Config.font_size_small - 10, offset, 0, '')
        label_clock.colour = Config.color_white

        # volume
        offset = offset + Config.font_size_small + 12
        VolumeBar(self.main, x_offset-5, offset, 100, 100, 12, Config.color_white)
        VolumeBar(self.main, x_offset+1-5, offset+1, 100, 100, 10, Config.color_black)
        bar2 = VolumeBar(self.main, x_offset+2-5, offset+2, self.main.volume, 100, 8, Config.color_white)

        offset = offset + 16
        label_vol = Program.write(self.font_small, x_offset, offset, 0, '')
        label_vol.colour = Config.color_white

        while True:

            current = self.main.get_micro()

            #todo: change scene request

            bar.value = self.main.channel + 1
            bar2.value = self.main.volume

            self.title = self.main.fetch_station_title()
            if self.last_title != self.title:
                label_station.text = self.title
                self.song = u'ЗАГРУЗКА...'
                self.last_title = self.title

            if current - self.last_song_fetch > Config.mpd_poll_timeout and self.main.need_change_song is False:
                song = self.main.fetch_song_title()
                if self.last_song != song:
                    self.song = song
                    self.last_song = song
                self.last_song_fetch = current

            part = textwrap.wrap(self.song, (self.main.screen_size[0]-16)/Config.font_size_small)
            if len(part) >= 4:
                label_song1.text = part[0]
                label_song2.text = part[1]
                label_song3.text = part[2]
                label_song4.text = part[3]
            elif len(part) >= 3:
                label_song1.text = part[0]
                label_song2.text = part[1]
                label_song3.text = part[2]
                label_song4.text = ''
            elif len(part) >= 2:
                label_song1.text = part[0]
                label_song2.text = part[1]
                label_song3.text = ''
                label_song4.text = ''
            else:
                label_song1.text = self.song
                label_song2.text = ''
                label_song3.text = ''
                label_song4.text = ''

            label_pos.text = u'СТАНЦИЯ: {0} / {1}'.format(self.main.channel+1, len(self.main.playlist.playlist))
            label_vol.text = u'ГРОМКОСТЬ: {0} %'.format(self.main.volume)

            # display time
            dt = datetime.datetime.now()
            hours = dt.strftime('%H')
            minutes = dt.strftime('%M')
            if current - self.last_blinked >= 500:
                self.last_blinked = current
                self.blinked = not self.blinked
            if self.blinked:
                blink = ':'
            else:
                blink = ' '
            label_clock.text = hours + blink + minutes

            yield

