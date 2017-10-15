"""
Sensor for Xbox Live account status using api.xboxrecord.us.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.xru_xbox_live/
"""
import logging
import voluptuous as vol
import urllib.request
import json
import re

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_API_KEY, STATE_UNKNOWN)
from homeassistant.helpers.entity import Entity


_LOGGER = logging.getLogger(__name__)

CONF_GAMERTAGS = 'gamertags'

ICON = 'mdi:xbox'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_GAMERTAGS): vol.All(cv.ensure_list, [cv.string])
})


# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Xbox platform."""
    devices = []
    _LOGGER.info('test')
    for gamertag in config.get(CONF_GAMERTAGS):
        _LOGGER.info(gamertag)
        new_device = XboxSensor(hass, gamertag)
        if new_device.success_init:
            devices.append(new_device)

    if devices:
        add_devices(devices)
    else:
        return False




class XboxSensor(Entity):
    """A class for the Xbox account."""

    def __init__(self, hass, gamertag):
        """Initialize the sensor."""
        self._hass = hass
        self._state = STATE_UNKNOWN
        self._presence = {}
        self._gamertag = gamertag

        # get profile info
        userDetails = self.fetch_user_details(self._gamertag)
        

        if userDetails['status'] == "success":
            self.update()
            self.success_init = True
            for item in userDetails['userDetails']:
                if (item['id'] == "GameDisplayPicRaw"):
                    pic = item['value']
                    pic = re.sub("http://images-eds", "https://images-eds-ssl", pic)
                    self._picture = self._picture = pic
        else:
            self.success_init = False

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._gamertag

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        attributes = {}
        #for device in self._presence:
        #    for title in device.get('titles'):
        #        attributes[
        #            '{} {}'.format(device.get('type'), title.get('placement'))
        #        ] = title.get('name')

        return attributes

    @property
    def entity_picture(self):
        """Avatar of the account."""
        return self._picture

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON

    def update(self):
        """Update state data from Xbox API."""
        presence = self.fetch_user_presence(self._gamertag)
        self._state = presence['userPresence'][0]['state']
        self._presence = presence

    def fetch_user_details(self, gamertag):
        """ Fetches user details """
        url = 'https://api.xboxrecord.us/userdetails/gamertag/{}'.format(gamertag)
        req = urllib.request.Request(url)
        raw_json = urllib.request.urlopen(req).read()
        data = json.loads(raw_json.decode('utf-8'))

        return data

    def fetch_user_presence(self, gamertag):
        """ Fetches user presence """
        url = 'https://api.xboxrecord.us/userpresence/gamertag/{}'.format(gamertag)
        req = urllib.request.Request(url)
        raw_json = urllib.request.urlopen(req).read()
        data = json.loads(raw_json.decode('utf-8'))

        return data