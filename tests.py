"""Testsq for Balloonicorn's Flask app."""

import unittest
import party
# from flask import session


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = party.app.test_client()
        party.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn(b"having a party", result.data)

    def test_no_rsvp_yet(self):
        """Do users who haven't RSVPed see the correct view?"""

        with self.client.session_transaction() as session:
            session['rsvp'] = False

        page = self.client.get('/')
        self.assertIn(b"Please RSVP", page.data)


    def test_rsvp(self):
        """Do RSVPed users see the correct view?"""

        rsvp_info = {'name': "Jane", 'email': "jane@jane.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)

        # FIXME: check that once we log in we see party details--but not the form!
        page = self.client.get('/')
        self.assertIn(b"Party Details", page.data)

    def test_rsvp_mel(self):
        """Can we keep Mel out?"""

        rsvp_info = {'name': 'mel', 'email': 'MEL@UBERMELON.COM'}
        result = self.client.post('/rsvp', data=rsvp_info,
                                  follow_redirects=True)

        self.assertIn(b'Sorry, Mel.', result.data)

    def test_rsvp_not_mel(self):
        """Can we let Mel-like names in?"""

        rsvp_info = {'name': 'Caramel', 'email': 'carmel@ubermelon.com'}
        result = self.client.post('/rsvp', data=rsvp_info,
                                  follow_redirects=True)

        self.assertNotIn(b'Sorry, Mel.', result.data)



if __name__ == "__main__":
    unittest.main()
