#!/usr/bin/env python
import cgi
import json
from mako.template import Template

print 'Content Type: "text/html"'
print

html = '''
<html>
<head>
<title>
% if player:
    ${player}
% else:
    Matchups
% endif
</title>
</head>
<body>
% if error:
    <b style='color: red'>${error}</b>
% elif player is None:
    <b>Players</b>
    <br>
    <ul>
    % for p in sorted(players):
        <li>${player_link(p)}</li>
    % endfor
    </ul>

% else:
    <b>${player} (${'{:.2f}'.format(win_pct)}%)</b>
    <br>

    <ul>
    % for opp, wl in opps:
        <li>${player_link(opp)}: ${wl}</li>
    % endfor
    </ul>
% endif

<%def name="player_link(p)">
<a href="matchups.py?name=${p}">${p}</a>
</%def>

</body>
</html>
'''

def winloss(results):
    wins = results.get('win', 0)
    losses = results.get('loss', 0)

    return '{} - {}'.format(wins, losses)

with open('player_matchups.json') as j:
    players = json.load(j)

form = cgi.FieldStorage()
player = form.getvalue('name')

if player is None:
    print Template(html).render(player=None,
                                players=players)
    exit()
else:
    player = player.title()

if player not in players:
    error = 'Player not found'

    print Template(html).render(error=error)
    exit()

error = None

matchups = players[player]
win_pct = matchups['win_pct']

opps = []
for opp, val in sorted(matchups.items()):
    if opp == 'win_pct':
        continue

    opps.append((opp, winloss(val)))

print Template(html).render(error=error,
                            player=player,
                            win_pct=win_pct,
                            opps=opps)
