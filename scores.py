import requests
import tkinter as tk
from tkinter import ttk

def fetch_scores():
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    response = requests.get(url)

    if response.status_code != 200:
        return [f"Failed to retrieve scores. Status code: {response.status_code}"]

    data = response.json()
    games = data.get("events", [])
    in_progress = [] #this shows games in progress
    finished = [] #this shows finished games

    for game in games:
        competitions = game.get("competitions", [])
        if not competitions:
            continue

        comp = competitions[0]
        competitors = comp.get("competitors", [])
        status = game.get("status", {}).get("type", {}).get("shortDetail", "")

        if len(competitors) == 2:
            team1 = competitors[0]["team"]["abbreviation"] # this is the name of the home team in scores
            score1 = competitors[0].get("score", "0")
            team2 = competitors[1]["team"]["abbreviation"] # this is the name of the away team in scores
            score2 = competitors[1].get("score", "0")
            score_text = f"{team1} {score1} - {team2} {score2} ({status})"

            # Separate in-progress and finished games
            if "In Progress" in status:
                in_progress.append(score_text)
            else:
                finished.append(score_text)

    # Combine in-progress games first, followed by finished games
    return in_progress + finished if in_progress else finished

def display_scores():
    listbox.delete(0, tk.END)
    scores = fetch_scores()
    for score in scores:
        listbox.insert(tk.END, score)

# GUI setup
root = tk.Tk()
root.title("MLB Live Scores")

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

listbox = tk.Listbox(frame, height=20, width=50)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

refresh_button = ttk.Button(root, text="Refresh Scores", command=display_scores)
refresh_button.pack(pady=5)


if __name__ == "__main__":
    display_scores()
    root.mainloop()