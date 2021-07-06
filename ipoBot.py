from typing import TypedDict
from webbot import Browser
import time;
from bs4 import BeautifulSoup

class MeroshareCredentials(TypedDict):
    username: str
    password: str
    participantId: str

class CompaniesWithIPOFetcher:
    def __init__(self, meroshareCredentials: MeroshareCredentials) -> None:
        self.web: Browser = Browser()
        self.meroshareCredentials: MeroshareCredentials = meroshareCredentials;

    def navigateToLink(self, link: str) -> None:
        self.web.go_to(link)

    def insertUsername(self) -> None:
        self.web.type(text=self.meroshareCredentials['username'], id='username')

    def insertPassword(self) -> None:
        self.web.type(text=self.meroshareCredentials['password'], id='password')

    def insertParticipant(self) -> None:
        self.web.click(tag='span', text='Select your DP', id='select2-c0mc-container')
        self.web.type(text = self.meroshareCredentials['participantId'], classname='select2-search__field')
        self.web.press(self.web.Key.ENTER)
        self.web.press(self.web.Key.ESCAPE)

    def attemptLogin(self) -> None:
        self.web.click(tag='button', text='Login')

    def navigateToASBAMenu(self) -> None:
        self.navigateToLink('https://meroshare.cdsc.com.np/#/asba')

    def extractCompanyNameFromHTMLString(self, htmlString: str) -> str:
        soup = BeautifulSoup(htmlString, 'html.parser')
        spanSoupElementsWithCompanyDetails = soup.find_all('span')
        spanSoupElementWithCompanyName = spanSoupElementsWithCompanyDetails[0]
        return spanSoupElementWithCompanyName.string.strip()

    def extractCompanyNamesWithIPO(self) -> list:
        # we are redirecting to new link while navigating to the ASBA menu.
        # Because of this, the page reference changes.
        # Sleeping the program for 1 sec in order to correct the reference.
        time.sleep(1)

        companyNames = []
        spanElementsWithCompaniesDetails = self.web.find_elements(classname='company-name', tag='span')
        for spanElementWithCompanyDetail in spanElementsWithCompaniesDetails:
            innerHtmlOfSpanElement = spanElementWithCompanyDetail.get_attribute('innerHTML')
            companyName = self.extractCompanyNameFromHTMLString(innerHtmlOfSpanElement)
            companyNames.append(companyName)
        return companyNames

    def closeBrowser(self) -> None:
        self.web.close_current_tab()

    def fetchIPOCompanies(self) -> list:
        self.navigateToLink('https://meroshare.cdsc.com.np/#/login')
        self.insertUsername()
        self.insertPassword()
        self.insertParticipant()
        self.attemptLogin()
        self.navigateToASBAMenu()
        companyNames = self.extractCompanyNamesWithIPO()
        self.closeBrowser()
        return companyNames

meroshareCredentials: MeroshareCredentials = {
    'username': 'meroshare_username',
    'password': 'meroshare_password',
    'participantId': 'meroshare_participantId'
}
fetcher = CompaniesWithIPOFetcher(meroshareCredentials)
print(fetcher.fetchIPOCompanies())