# coding: utf-8

from datetime import timedelta as td

from django.utils.timezone import now
from hc.api.models import Channel, Check, Notification
from hc.test import BaseTestCase
from django.test.utils import override_settings


class NotifyMattermostTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.check = Check(project=self.project)
        self.check.status = "down"
        self.check.last_ping = now() - td(minutes=61)
        self.check.save()

        self.channel = Channel(project=self.project)
        self.channel.kind = "mattermost"
        self.channel.value = "123"
        self.channel.save()
        self.channel.checks.add(self.check)

    @override_settings(MATTERMOST_ENABLED=False)
    def test_it_requires_mattermost_enabled(self):
        self.channel.notify(self.check)

        n = Notification.objects.get()
        self.assertEqual(n.error, "Mattermost notifications are not enabled.")
