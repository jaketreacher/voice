from bs4 import BeautifulSoup

from django.test import TestCase
from django.shortcuts import reverse

from seed import factory


class TestLoginRedirect(TestCase):
    def test_admin_redirect_to_team_list(self):
        admin = factory.AdminFactory()
        self.client.force_login(user=admin.user)
        response = self.client.get(reverse('login-redirect'))
        self.assertRedirects(response, reverse('teams'))

    def test_mentor_redirect_to_candidate_list(self):
        factory.TeamFactory()
        mentor = factory.MentorFactory()
        self.client.force_login(user=mentor.user)
        response = self.client.get(reverse('login-redirect'))
        self.assertRedirects(response, reverse('candidates'))


class TestTeamView(TestCase):
    @staticmethod
    def scrape_table(html):
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.select('table tbody')[0]

        team_names = []
        for row in table.find_all('tr'):
            team_names.append(row.find_all('td')[0].text)
        return team_names

    def test_admin_see_all_teams(self):
        admin = factory.AdminFactory()
        self.client.force_login(user=admin.user)
        teams = factory.TeamFactory.create_batch(3)
        expected_team_names = [team.name for team in teams]

        response = self.client.get(reverse('teams'))
        self.assertEqual(response.status_code, 200)

        team_names = self.scrape_table(response.content)
        self.assertCountEqual(team_names, expected_team_names)

    def test_mentor_see_own_teams_only(self):
        teams = factory.TeamFactory.create_batch(2)
        expected_team_names = [team.name for team in teams]
        mentor = factory.MentorFactory()
        mentor.teams.set(teams)
        self.client.force_login(user=mentor.user)
        factory.TeamFactory.create_batch(2)

        response = self.client.get(reverse('teams'))
        self.assertEqual(response.status_code, 200)

        team_names = self.scrape_table(response.content)
        self.assertCountEqual(team_names, expected_team_names)
