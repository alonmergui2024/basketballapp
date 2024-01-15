import requests
from bs4 import BeautifulSoup
from datetime import datetime

current_date = datetime.now()
formatted_date = current_date.strftime("%Y%m%d")
URL = "https://www.espn.com/nba/teams"
header = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}
response = requests.get(URL, headers=header)
s = BeautifulSoup(response.content, "html.parser")
results = s.find(id="fitt-analytics")


class Autocomplete:
    def __init__(self, team):
        self.team = team

    def suggest(self, prefix):
        prefix = prefix.lower()
        suggestions = []
        for word in self.team:
            for miniword in word.split(" "):
                if miniword.lower().startswith(prefix.lower()) or miniword.lower() == prefix.lower():
                    suggestions.append(word)
                    break

        return suggestions


if results:
    team = []
    teams = results.find_all('h2', class_='di clr-gray-01 h5')
    for i in teams:
        team.append(i.text)
    autocomplete_engine = Autocomplete(team)
option1 = ["this week games", "all games"]
autocomplete_engine1 = Autocomplete(option1)

def register():
    users = open("users.text", "r")
    username = input("Create username: ")
    password = input("Create password: ")
    password1 = input("Confirm password: ")
    d = []
    f = []
    g = []
    for i in users:
        if "," in i:
            a, b, c = i.split(",")
            b = b.strip()
            d.append(a)
            f.append(b)
            g.append(c)
        else:
            pass
        data = dict(zip(d, f))
        data1 = dict(zip(data, g))

    if password != password1:
        print("Passwords are not the same, please try again")
        register()
    else:
        if len(password) < 6:
            print("Password are too short, please try again")
            register()
        elif username in d:
            print("Username already exist, please try again")
            register()
        else:
            users = open("users.text", "a")
            print("Success!\n\n")
            print("Welcome " + username + ",")
            choice = input("Want to choose your favorite team right now? ")
            if choice.lower() == "yes":
                suggestions1 = ""
                while not suggestions1:
                    fav = input("Enter your favorite team: ")
                    suggestions1 = autocomplete_engine.suggest(fav)
                    data1[username] = suggestions1
                    if suggestions1:
                        users.write(username + "," + password + "," + suggestions1[0] + "\n")
                        print("Favorite team updated successfully to", suggestions1[0])
                        return data1[username]
                    else:
                        print("the team is not found. please check the team name...")
                        register()

            elif choice.lower() == "no":
                print("Ok you can always do this later")
                users.write(username + "," + password + "," + " " + "\n")
                return data1[username]

            else:
                print("Please enter only yes or no")
                register()







def access():
    users = open("users.text", "r")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if len(username) > 0 and len(password) > 0:
        d = []
        f = []
        g = []
        for i in users:
            if "," in i:
                a, b, c = i.split(",")
                b = b.strip()
                d.append(a)
                f.append(b)
                g.append(c)
            else:
                pass
        data = dict(zip(d, f))
        data1 = dict(zip(data, g))

        try:
            if data[username]:
                try:
                    if password == data[username]:
                        print("Login success\n\n")
                        print("Welcome back " + username + ",")

                        if not data1[username]:
                            choice = input(
                                "It looks like you haven't set your favorite team. Do you want to do it now? ")
                            if choice.lower().strip() == "yes":
                                suggestions1 = ""
                                while not suggestions1:
                                    fav = input("Enter your favorite team: ")
                                    suggestions1 = autocomplete_engine.suggest(fav)
                                    if suggestions1:
                                        users.write(username + "," + password + "," + suggestions1[0] + "\n")
                                        data1[username] = suggestions1
                                        with open("users.text", "w") as users_file:
                                            for user, password, fav_team in zip(d, f, g):
                                                users_file.write(user + "," + password + "," + suggestions1 + "\n")
                                            print("Favorite team updated successfully to", suggestions1[0])
                                            return data1[username]
                                    else:
                                        print("the team is not found. please check the team name...")
                                        access()
                            elif choice.lower().strip() == "no":
                                print("Ok you can always do this later")
                                users.write(username + "," + password + "," + " " + "\n")
                                return data1[username]
                            else:
                                print("Please write only yes or no")
                                access()
                        else:
                            print("It looks like your favorite team is:", data1[username])
                            return data1[username]
                    else:
                        print("Username or password incorrect")
                        access()
                except:
                    print("Username or password incorrect")
                    access()
            else:
                print("Username or password incorrect")
                access()
        except:
            print("Username or password incorrect")
            access()


def home():
    print("Signup | Login | guest ")
    option = input()
    if option.lower() == "login":
        fav_team = access()
        return fav_team
    elif option.lower() == "signup":
        fav_team = register()
        return fav_team
    elif option.lower() == "guest":
        pass

fav_team = home()
if fav_team:
    print("here are the games of your favorite team:")
    print("here are your favorite team this week games:")
    autocomplete_engine2 = Autocomplete(team)
    url = f"https://www.espn.com/nba/schedule/_/date/{formatted_date}"
    response1 = requests.get(url, headers=header)
    s1 = BeautifulSoup(response1.content, "html.parser")
    results1 = s1.find(id="fittPageContainer")
    table = results1.find_all("div", class_="ScheduleTables mb5 ScheduleTables--nba ScheduleTables--basketball")
    teams1 = results1.find_all("td", class_="events__col Table__TD")
    teams2 = results1.find_all("td", class_="colspan__col Table__TD")
    times = results1.find_all("td", class_="date__col Table__TD")
    games = list(zip(teams1, teams2, times))
    table = [element for element in table if
             "teams__col Table__TD" and "teams__col Table__TD" and "leaders__col Table__TD" and "broadcast__col Table__TD" and "tickets__col Table__TD" not in element.attrs.get(
                 "class", [])]
    '''
    for i in table:
        print(i.text.strip())
    '''
    for x, y, z in games:
        team1 = x.text.strip().split()
        team2 = y.text.strip().split()
        time = z.text.strip()
        suggestions2 = autocomplete_engine2.suggest(team1[0])
        suggestions3 = autocomplete_engine2.suggest(team2[1])
        if suggestions3[0] == fav_team.strip() or suggestions2[0] == fav_team.strip():
            g = f'{x.text}{y.text} {time}'
            print(g.replace('@', 'vs'))
else:
    pass
user_input = input("witch team do you want to see? ")
suggestions = autocomplete_engine.suggest(user_input.split(" ")[0])

if suggestions:
    while len(suggestions) > 1:
        print(suggestions)
        user_input = input("witch team did you mean? ")
        suggestions = autocomplete_engine.suggest(user_input)
    print(suggestions[0].strip())
    autocomplete_engine2 = Autocomplete(suggestions)
    user_input1 = input("what do you want to see? (this week games or all games) ")
    output = autocomplete_engine1.suggest(user_input1.split(" ")[0])
    print(output[0].strip())

    if output[0].strip() == option1[0]:
        url = f"https://www.espn.com/nba/schedule/_/date/{formatted_date}"
        response1 = requests.get(url, headers=header)
        s1 = BeautifulSoup(response1.content, "html.parser")
        results1 = s1.find(id="fittPageContainer")
        table = results1.find_all("div", class_="ScheduleTables mb5 ScheduleTables--nba ScheduleTables--basketball")
        teams1 = results1.find_all("td", class_="events__col Table__TD")
        teams2 = results1.find_all("td", class_="colspan__col Table__TD")
        times = results1.find_all("td", class_="date__col Table__TD")
        games = list(zip(teams1, teams2, times))
        table = [element for element in table if
                 "teams__col Table__TD" and "teams__col Table__TD" and "leaders__col Table__TD" and "broadcast__col Table__TD" and "tickets__col Table__TD" not in element.attrs.get(
                     "class", [])]
        '''
        for i in table:
            print(i.text.strip())
        '''
        for x, y, z in games:
            team1 = x.text.replace('@', '').strip().split()
            team2 = y.text.replace('@', '').strip().split()
            time = z.text.strip()
            suggestions2 = autocomplete_engine2.suggest(team1[0])
            suggestions3 = autocomplete_engine2.suggest(team2[1])
            if suggestions3 or suggestions2:
                g = f'{x.text}{y.text} {time}'
                print(g.replace('@', 'vs'))
